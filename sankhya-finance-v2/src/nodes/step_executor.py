"""
StepExecutor Node - Executes one decomposition step at a time.

This node processes the step at state["current_step_index"] from the
plan in state["steps"]. It handles two types of steps:

    DATA steps:
        - Looks up the tool by name from TOOLS_BY_NAME (21 tools across
          5 sources: YFinance, SEC EDGAR, FRED, FMP, DuckDuckGo)
        - Calls the tool with the specified parameters
        - Stores a typed StepResult in state["step_results"][step_id]

    ANALYSIS steps:
        - Gathers data from dependency steps (from step_results)
        - Sends the analysis_prompt + gathered data to the LLM
        - Stores a typed StepResult in state["step_results"][step_id]
        - The final step is always "final_synthesis" which synthesizes
          all findings into a direct answer to the user's question

If the Verifier previously returned NEEDS_MORE_DATA with a retry_step,
this node executes the modified retry_step instead of the original.

Graph position:
    Decomposer -> [this node] -> Verifier
                      ▲              │
                      │   NEEDS_MORE_DATA (retry with modified params, max 2)
                      └──────────────┘
                      ▲
                      │   AdvanceIndex -> [this node] (next step)
                      └──────────────────────────────┘

This node does NOT decide what to do next -- it just executes and reports.
The VerifierNode handles all routing decisions.
"""

import json
from typing import Any

from langchain_core.messages import HumanMessage

from src.state import (
    FinanceState,
    DecompositionStep,
    StepResult,
    StepType,
    Verdict,
    VerificationResult,
)
from src.tools.yfinance_tools import TOOLS_BY_NAME
from src.utils.model_config import get_llm


# =============================================================================
# Node Function
# =============================================================================


async def step_executor(state: FinanceState) -> dict[str, Any]:
    """
    Execute the current step from the decomposition plan.

    Reads state["current_step_index"] to find which step to execute.
    Validates dependencies are satisfied, then dispatches to the
    appropriate handler based on step_type.

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with typed StepResult, any errors, and messages.
    """
    steps: list[DecompositionStep] = state.get("steps", [])
    step_index: int = state.get("current_step_index", 0)
    step_results: dict[str, StepResult] = dict(state.get("step_results", {}))

    # --- Safety check: is there a step to execute? ---
    if step_index >= len(steps):
        return {
            "current_step_error": "No more steps to execute",
            "messages": state.get("messages", []) + [
                f"[StepExecutor] No step at index {step_index} (total: {len(steps)})"
            ],
            "total_node_calls": state.get("total_node_calls", 0) + 1,
        }

    step: DecompositionStep = steps[step_index]

    # --- Check if this is a retry with a modified step from the Verifier ---
    verification: VerificationResult | None = state.get("verification")
    if (
        verification
        and isinstance(verification, VerificationResult)
        and verification.verdict == Verdict.NEEDS_MORE_DATA
        and verification.retry_step is not None
    ):
        # The Verifier provided a modified step to retry
        step = verification.retry_step

    # --- Execute based on step type ---
    try:
        if step.step_type == StepType.DATA:
            result = await _execute_data_step(step)
        elif step.step_type == StepType.ANALYSIS:
            result = await _execute_analysis_step(step, step_results)
        else:
            result = StepResult(
                step_id=step.step_id,
                step_type=step.step_type,
                success=False,
                error=f"Unknown step type: {step.step_type}",
            )

        # --- Store result ---
        step_results[step.step_id] = result

        # --- Return state update ---
        error_msg = result.error or ""
        return {
            "step_results": step_results,
            "current_step_error": error_msg,
            "messages": state.get("messages", []) + [
                f"[StepExecutor] Executed {step.step_id} ({step.step_type.value}): "
                f"{'ERROR: ' + error_msg if error_msg else 'success'}"
            ],
            "total_node_calls": state.get("total_node_calls", 0) + 1,
        }

    except Exception as e:
        # Unexpected exception -- create a failed StepResult
        error_msg = f"Exception in {step.step_id}: {str(e)}"
        failed_result = StepResult(
            step_id=step.step_id,
            step_type=step.step_type,
            success=False,
            error=error_msg,
        )
        step_results[step.step_id] = failed_result

        return {
            "step_results": step_results,
            "current_step_error": error_msg,
            "messages": state.get("messages", []) + [
                f"[StepExecutor] EXCEPTION in {step.step_id}: {e}"
            ],
            "total_node_calls": state.get("total_node_calls", 0) + 1,
        }


# =============================================================================
# Step Type Handlers
# =============================================================================


async def _execute_data_step(step: DecompositionStep) -> StepResult:
    """
    Execute a DATA step by calling the appropriate YFinance tool.

    Returns a typed StepResult with the data or error.
    """
    # --- Validate tool exists ---
    if not step.tool_name:
        return StepResult(
            step_id=step.step_id,
            step_type=StepType.DATA,
            success=False,
            error=f"DATA step '{step.step_id}' missing tool_name",
        )

    tool_fn = TOOLS_BY_NAME.get(step.tool_name)
    if not tool_fn:
        available = list(TOOLS_BY_NAME.keys())
        return StepResult(
            step_id=step.step_id,
            step_type=StepType.DATA,
            success=False,
            error=f"Unknown tool '{step.tool_name}'. Available: {available}",
        )

    # --- Call the tool ---
    raw_result = tool_fn.invoke(step.parameters)

    # --- Check for tool-level errors ---
    if isinstance(raw_result, dict) and "error" in raw_result:
        return StepResult(
            step_id=step.step_id,
            step_type=StepType.DATA,
            success=False,
            data=raw_result,  # Keep the error dict for context
            error=raw_result["error"],
        )

    return StepResult(
        step_id=step.step_id,
        step_type=StepType.DATA,
        success=True,
        data=raw_result,
    )


async def _execute_analysis_step(
    step: DecompositionStep,
    step_results: dict[str, StepResult],
) -> StepResult:
    """
    Execute an ANALYSIS step by sending data + prompt to the LLM.

    Gathers typed StepResults from dependency steps, includes their
    data in the prompt, and asks the LLM to analyze.
    """
    analysis_prompt = step.analysis_prompt or "Analyze the available data."

    # --- Gather data from dependency steps using typed access ---
    dependency_data: dict[str, str] = {}
    for dep_id in step.depends_on:
        if dep_id in step_results:
            dep_result: StepResult = step_results[dep_id]
            dependency_data[dep_id] = dep_result.get_data_for_prompt()
        else:
            dependency_data[dep_id] = f"<data not available for {dep_id}>"

    # --- Build the full prompt ---
    data_context = json.dumps(dependency_data, indent=2, default=str)
    full_prompt = f"""{analysis_prompt}

Available Data from Previous Steps:
{data_context}

Please provide a detailed, specific analysis based on this data.
Include actual numbers, percentages, and calculations where relevant.
Be concise but thorough."""

    # --- Call the LLM ---
    llm = get_llm(temperature=0.1)
    response = await llm.ainvoke([HumanMessage(content=full_prompt)])

    return StepResult(
        step_id=step.step_id,
        step_type=StepType.ANALYSIS,
        success=True,
        analysis=response.content,
    )
