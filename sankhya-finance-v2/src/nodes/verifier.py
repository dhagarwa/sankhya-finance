"""
Verifier Node - LLM-powered quality check after every step execution.

This is the "quality control" node that runs AFTER every StepExecutor call.
It ALWAYS calls the LLM to evaluate the step result -- no shortcircuits.

The LLM inspects the result and returns a structured verdict:

    OK              -> The step result is good quality and answers what was needed.
                       If more steps remain, advance to the next step.
                       If all steps are done, go to OutputFormatter.

    NEEDS_MORE_DATA -> The step result is incomplete, has errors, or is missing
                       important information. Go back to StepExecutor with a
                       modified retry_step that has corrected parameters.

    REPLAN          -> The entire decomposition plan is fundamentally wrong
                       (e.g., wrong tickers, wrong approach, wrong tools).
                       Go back to the Decomposer to create a new plan.

Safety limits:
    - retry_count:  tracks retries per step (max 2), then force OK
    - replan_count: explicit counter in state (max 1), then force OK
    - recursion_limit: set at graph compile time as final backstop
"""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.state import (
    FinanceState,
    DecompositionStep,
    StepResult,
    StepType,
    Verdict,
    VerificationResult,
)
from src.utils.model_config import get_llm


# =============================================================================
# Constants
# =============================================================================

MAX_RETRIES_PER_STEP = 2    # Max times to retry a single step
MAX_REPLANS = 1              # Max times to go back to decomposer


# =============================================================================
# Verification Prompt
# =============================================================================
# This prompt is sent to the LLM for EVERY step result, without exception.
# The LLM acts as a thorough quality checker that verifies:
#   - Data completeness (are all expected fields present?)
#   - Data freshness (are dates reasonable?)
#   - Data correctness (are numbers in sane ranges?)
#   - Relevance (does this data actually help answer the user's query?)
# =============================================================================

VERIFICATION_PROMPT = """You are a meticulous financial data quality expert. Your job is to thoroughly verify whether a step in a financial analysis pipeline produced a GOOD, ACCURATE, and COMPLETE result.

ORIGINAL USER QUERY: "{query}"

FULL DECOMPOSITION PLAN:
{plan_summary}

CURRENT STEP BEING VERIFIED:
  Step ID: {step_id}
  Description: {step_description}
  Type: {step_type}
  Tool Used: {tool_name}
  Parameters: {parameters}

STEP RESULT:
{step_result}

ALL PREVIOUS STEP RESULTS (for context):
{previous_results}

RETRY INFORMATION:
  Times retried so far: {retry_count} (max allowed: {max_retries})

---

Perform a THOROUGH quality check:

1. **Completeness**: Does the result contain all the data needed for this step's purpose?
   - For DATA steps: Are the key financial fields present and non-null?
   - For ANALYSIS steps: Does the analysis address the original question with specific numbers?

2. **Correctness**: Do the values look reasonable?
   - Stock prices should be positive numbers
   - Market caps should be in billions/trillions for large companies
   - Percentages should be in reasonable ranges
   - Dates should be recent (not stale data from years ago)

3. **Relevance**: Does this result actually help answer the user's query?
   - Is the right company/ticker being analyzed?
   - Is the right time period covered?
   - Is the right metric being fetched?

4. **Error Check**: Is there any error in the result?
   - Explicit error messages
   - Empty data or null values where data was expected
   - Timeouts or API failures

Based on your assessment, return a JSON object with ONE of these verdicts:

VERDICT 1 - Result is good:
{{"verdict": "ok", "explanation": "Detailed explanation of why this result passes quality checks"}}

VERDICT 2 - Result needs retry with different parameters (only if retry_count < {max_retries}):
{{"verdict": "needs_more_data", "explanation": "What specifically is wrong or missing", "additional_request": "What data to fetch differently", "retry_step": {{"step_id": "{step_id}", "description": "Retry description", "step_type": "{step_type}", "tool_name": "exact_tool_name", "parameters": {{"ticker": "...", ...}}}}}}

VERDICT 3 - The entire plan approach is wrong:
{{"verdict": "replan", "explanation": "What's fundamentally wrong", "replan_reason": "Why the decomposition plan needs to be redesigned"}}

IMPORTANT RULES:
- If retry_count >= {max_retries}, you MUST return "ok" even if the result isn't perfect. We need to move forward.
- Only use "replan" if the APPROACH is wrong (wrong tickers, wrong tools), not just if data is slightly incomplete
- For "needs_more_data", you MUST provide a complete retry_step with valid tool_name and parameters
- Be thorough but practical: partial data is acceptable if it's enough to answer the query

Return ONLY valid JSON, no additional text."""


# =============================================================================
# Node Function
# =============================================================================


async def verifier(state: FinanceState) -> dict[str, Any]:
    """
    LLM-powered verification of the most recently executed step.

    ALWAYS calls the LLM -- no shortcircuit checks. Accuracy over speed.

    This node:
        1. Gets the current step and its typed StepResult from state
        2. Sends the full context to the LLM for thorough evaluation
        3. Parses the LLM's verdict into a typed VerificationResult
        4. Returns the result which drives conditional edge routing

    Args:
        state: The current FinanceState.

    Returns:
        Partial state update with VerificationResult and updated counters.
    """
    steps: list[DecompositionStep] = state.get("steps", [])
    step_index: int = state.get("current_step_index", 0)
    step_results: dict[str, StepResult] = state.get("step_results", {})
    retry_count: int = state.get("retry_count", 0)
    replan_count: int = state.get("replan_count", 0)

    # --- Get the current step and its result ---
    if step_index >= len(steps):
        return {
            "verification": VerificationResult(
                verdict=Verdict.OK,
                explanation="No more steps to verify",
            ),
            "messages": state.get("messages", []) + [
                "[Verifier] No more steps to verify"
            ],
            "total_node_calls": state.get("total_node_calls", 0) + 1,
        }

    step: DecompositionStep = steps[step_index]
    step_result: StepResult | None = step_results.get(step.step_id)

    # --- Build plan summary for context ---
    plan_summary = "\n".join(
        f"  {s.step_id} ({s.step_type.value}): {s.description}"
        for s in steps
    )

    # --- Build previous results context ---
    previous_results_str = ""
    for prev_id, prev_result in step_results.items():
        if prev_id != step.step_id and isinstance(prev_result, StepResult):
            data_str = prev_result.get_data_for_prompt()
            # Truncate large results
            if len(data_str) > 500:
                data_str = data_str[:500] + "... (truncated)"
            previous_results_str += f"\n  {prev_id} ({prev_result.step_type.value}): {data_str}\n"

    if not previous_results_str:
        previous_results_str = "  (no previous results yet)"

    # --- Build the step result string ---
    if step_result and isinstance(step_result, StepResult):
        step_result_str = step_result.get_data_for_prompt()
    else:
        step_result_str = "<no result available>"

    # --- Build the prompt ---
    prompt = VERIFICATION_PROMPT.format(
        query=state.get("query", ""),
        plan_summary=plan_summary,
        step_id=step.step_id,
        step_description=step.description,
        step_type=step.step_type.value,
        tool_name=step.tool_name or "N/A (ANALYSIS step)",
        parameters=json.dumps(step.parameters, default=str) if step.parameters else "N/A",
        step_result=step_result_str[:3000],  # Cap length for context
        previous_results=previous_results_str[:2000],
        retry_count=retry_count,
        max_retries=MAX_RETRIES_PER_STEP,
    )

    # --- Call the LLM ---
    llm = get_llm(temperature=0, max_tokens=1500)

    try:
        response = await llm.ainvoke([
            SystemMessage(
                content=(
                    "You are a meticulous financial data quality verification expert. "
                    "Evaluate the step result thoroughly. Return only valid JSON."
                )
            ),
            HumanMessage(content=prompt),
        ])

        # Parse the response
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        raw_verdict = json.loads(content.strip())

    except (json.JSONDecodeError, Exception) as e:
        # If we can't parse the LLM response, default to OK to avoid blocking
        raw_verdict = {
            "verdict": "ok",
            "explanation": f"Verification LLM response couldn't be parsed: {e}. Proceeding.",
        }

    # --- Convert raw verdict to typed VerificationResult ---
    verdict_str = raw_verdict.get("verdict", "ok").lower()

    # Map to our Verdict enum
    try:
        verdict = Verdict(verdict_str)
    except ValueError:
        verdict = Verdict.OK  # Unknown verdict -> proceed

    # --- Apply safety limits ---

    # If retries exhausted, force OK regardless of LLM opinion
    if verdict == Verdict.NEEDS_MORE_DATA and retry_count >= MAX_RETRIES_PER_STEP:
        verdict = Verdict.OK
        raw_verdict["explanation"] = (
            f"LLM wanted retry but max retries ({MAX_RETRIES_PER_STEP}) reached. "
            f"Moving forward with available data."
        )

    # If replans exhausted, force OK regardless of LLM opinion
    if verdict == Verdict.REPLAN and replan_count >= MAX_REPLANS:
        verdict = Verdict.OK
        raw_verdict["explanation"] = (
            f"LLM wanted replan but max replans ({MAX_REPLANS}) reached. "
            f"Moving forward with current plan."
        )

    # --- Build the typed VerificationResult ---
    # Parse retry_step if provided
    retry_step: DecompositionStep | None = None
    if verdict == Verdict.NEEDS_MORE_DATA and "retry_step" in raw_verdict:
        try:
            rs = raw_verdict["retry_step"]
            raw_type = rs.get("step_type", "DATA").upper()
            try:
                rs_type = StepType(raw_type)
            except ValueError:
                rs_type = StepType.DATA

            retry_step = DecompositionStep(
                step_id=rs.get("step_id", step.step_id),
                description=rs.get("description", step.description),
                step_type=rs_type,
                tool_name=rs.get("tool_name", step.tool_name),
                parameters=rs.get("parameters", step.parameters),
                analysis_prompt=rs.get("analysis_prompt", step.analysis_prompt),
                depends_on=rs.get("depends_on", step.depends_on),
            )
        except Exception:
            # If we can't parse retry_step, fall back to OK
            verdict = Verdict.OK
            raw_verdict["explanation"] += " (retry_step couldn't be parsed, proceeding)"

    verification = VerificationResult(
        verdict=verdict,
        explanation=raw_verdict.get("explanation", ""),
        additional_request=raw_verdict.get("additional_request"),
        retry_step=retry_step,
        replan_reason=raw_verdict.get("replan_reason"),
    )

    # --- Update retry count ---
    new_retry_count = retry_count
    if verdict == Verdict.NEEDS_MORE_DATA:
        new_retry_count = retry_count + 1
    elif verdict == Verdict.OK:
        new_retry_count = 0  # Reset for next step

    return {
        "verification": verification,
        "retry_count": new_retry_count,
        "messages": state.get("messages", []) + [
            f"[Verifier] Step {step.step_id}: verdict={verdict.value}, "
            f"explanation={verification.explanation[:150]}"
        ],
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }


# =============================================================================
# Routing Function (used by conditional edge in graph.py)
# =============================================================================


def route_after_verification(state: FinanceState) -> str:
    """
    Conditional edge function: decide where to go after verification.

    This is the KEY routing logic that enables the graph's self-correcting
    behavior. Based on the verifier's typed VerificationResult:

        NEEDS_MORE_DATA -> go back to "executor" to retry with modified params
        REPLAN          -> go back to "decomposer" to create a new plan
        OK + more steps -> go to "advance_and_execute" then "executor"
        OK + all done   -> go to "output_formatter" to produce final output

    Returns:
        The name of the next node to execute.
    """
    verification: VerificationResult | None = state.get("verification")

    # Handle case where verification hasn't been set
    if not verification or not isinstance(verification, VerificationResult):
        return "output_formatter"

    verdict = verification.verdict

    # --- Retry: go back to executor with modified step ---
    if verdict == Verdict.NEEDS_MORE_DATA:
        return "executor"

    # --- Replan: go back to decomposer ---
    if verdict == Verdict.REPLAN:
        return "decomposer"

    # --- OK: advance to next step or finish ---
    steps = state.get("steps", [])
    current_index = state.get("current_step_index", 0)

    if current_index + 1 < len(steps):
        return "advance_and_execute"
    else:
        return "output_formatter"


async def advance_step_index(state: FinanceState) -> dict[str, Any]:
    """
    Tiny helper node that increments current_step_index.

    We need this as a separate node because the Verifier sets the verdict
    and the routing function reads it -- the index must be incremented
    AFTER routing decides to advance.

    Flow: Verifier -> [this helper] -> StepExecutor
    """
    return {
        "current_step_index": state.get("current_step_index", 0) + 1,
        "verification": VerificationResult(verdict=Verdict.OK),  # Clear
        "current_step_error": "",
        "total_node_calls": state.get("total_node_calls", 0) + 1,
    }
