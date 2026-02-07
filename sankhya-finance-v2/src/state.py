"""
State Definition for the Sankhya Finance LangGraph Agent.

This module defines the FinanceState TypedDict and all supporting
Pydantic models that enforce structure on the data flowing through
the graph.

Design principles:
    1. Every complex field uses a Pydantic model (not dict[str, Any])
    2. Step results are tagged by type (DATA vs ANALYSIS) so consumers
       always know what they're getting
    3. Verification results use a proper model with typed verdict
    4. The state TypedDict references these models by type, not "Any"
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional, TypedDict

from pydantic import BaseModel, Field


# =============================================================================
# Enums -- constrained string types
# =============================================================================


class QueryType(str, Enum):
    """Whether the query needs financial data or can be answered directly."""
    FINANCIAL = "financial"
    NON_FINANCIAL = "non_financial"
    UNKNOWN = ""  # Not yet classified


class StepType(str, Enum):
    """The two kinds of steps the executor can handle."""
    DATA = "DATA"          # Calls a YFinance tool
    ANALYSIS = "ANALYSIS"  # Calls the LLM to reason about data


class Verdict(str, Enum):
    """The three possible outcomes from the Verifier."""
    OK = "ok"                       # Step result is good, proceed
    NEEDS_MORE_DATA = "needs_more_data"  # Retry with different params
    REPLAN = "replan"               # Go back to decomposer


# =============================================================================
# Pydantic Models -- structured data that flows through the graph
# =============================================================================


class DecompositionStep(BaseModel):
    """
    A single step in the query decomposition plan.

    Each step has a type that determines how the executor will handle it:
        - DATA:     Calls a YFinance tool to fetch raw financial data.
                    Must have tool_name and parameters set.
        - ANALYSIS: Calls the LLM to reason about previously fetched data.
                    Must have analysis_prompt set.

    The depends_on field lists step_ids whose results this step needs.
    The executor validates that all dependencies have completed successfully
    before executing this step.
    """

    step_id: str = Field(description="Unique identifier, e.g. 'step_1'")
    description: str = Field(description="Human-readable description of what this step does")
    step_type: StepType = Field(description="DATA or ANALYSIS")

    # --- DATA step fields ---
    tool_name: Optional[str] = Field(
        default=None,
        description="For DATA steps: exact name of the YFinance tool to call"
    )
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="For DATA steps: parameters to pass to the tool"
    )

    # --- ANALYSIS step fields ---
    analysis_prompt: Optional[str] = Field(
        default=None,
        description="For ANALYSIS steps: prompt describing what to calculate/interpret"
    )

    # --- Dependencies ---
    depends_on: list[str] = Field(
        default_factory=list,
        description="Step IDs whose results this step needs before it can execute"
    )

    def validate_for_execution(self) -> str | None:
        """
        Check that this step has the required fields for its type.

        Returns:
            None if valid, or an error message string if invalid.
        """
        if self.step_type == StepType.DATA:
            if not self.tool_name:
                return f"DATA step '{self.step_id}' is missing tool_name"
        elif self.step_type == StepType.ANALYSIS:
            if not self.analysis_prompt:
                return f"ANALYSIS step '{self.step_id}' is missing analysis_prompt"
        return None


class StepResult(BaseModel):
    """
    The result of executing a single step.

    Tagged by step_type so consumers always know what they're getting:
        - DATA results have data (dict from YFinance) and no analysis
        - ANALYSIS results have analysis (str from LLM) and no data
        - Failed steps have error set

    This replaces the old dict[str, Any] where DATA returned dicts
    and ANALYSIS returned strings with no way to distinguish them.
    """

    step_id: str = Field(description="Which step produced this result")
    step_type: StepType = Field(description="DATA or ANALYSIS")
    success: bool = Field(description="Whether the step completed without errors")

    # --- DATA step result ---
    data: Optional[dict[str, Any]] = Field(
        default=None,
        description="For DATA steps: the raw data dict from YFinance"
    )

    # --- ANALYSIS step result ---
    analysis: Optional[str] = Field(
        default=None,
        description="For ANALYSIS steps: the LLM's analysis text"
    )

    # --- Error ---
    error: Optional[str] = Field(
        default=None,
        description="Error message if the step failed"
    )

    def get_data_for_prompt(self) -> str:
        """
        Get a string representation of this result suitable for
        including in an LLM prompt (e.g., for dependent ANALYSIS steps
        or for the Verifier).
        """
        if self.error:
            return f"[ERROR] {self.error}"
        if self.data is not None:
            import json
            return json.dumps(self.data, indent=2, default=str)
        if self.analysis is not None:
            return self.analysis
        return "[No result data]"


class VerificationResult(BaseModel):
    """
    The Verifier's assessment of a step result.

    The verdict field drives conditional edge routing in the graph:
        - OK              -> proceed to next step (or formatter if done)
        - NEEDS_MORE_DATA -> go back to executor with retry_step
        - REPLAN          -> go back to decomposer with replan_reason
    """

    verdict: Verdict = Field(description="ok | needs_more_data | replan")
    explanation: str = Field(
        default="",
        description="Why the verifier made this decision"
    )

    # --- For NEEDS_MORE_DATA ---
    additional_request: Optional[str] = Field(
        default=None,
        description="What extra data/action is needed"
    )
    retry_step: Optional[DecompositionStep] = Field(
        default=None,
        description="Modified step to retry with corrected parameters"
    )

    # --- For REPLAN ---
    replan_reason: Optional[str] = Field(
        default=None,
        description="Why the entire plan needs to change"
    )


# =============================================================================
# Main Graph State
# =============================================================================
# LangGraph requires a TypedDict for the state schema.
# We use our Pydantic models as the field types so that every node
# works with structured, validated data instead of raw dicts.
#
# IMPORTANT: LangGraph merges the returned dict into the existing state,
# so nodes only need to return the fields they want to change.
# =============================================================================


class FinanceState(TypedDict, total=False):
    """
    The shared state that flows through every node in the finance graph.

    Fields are grouped by which node primarily writes them.
    Complex fields use Pydantic models instead of dict[str, Any].
    """

    # --- Input (set at invocation) ---
    query: str

    # --- Written by QueryRouter ---
    query_type: QueryType

    # --- Written by DirectResponseNode ---
    direct_response: str

    # --- Written by DecomposerNode ---
    steps: list[DecompositionStep]       # Proper typed list, not list[dict]
    decomposition_reasoning: str
    detected_tickers: list[str]

    # --- Written by StepExecutorNode ---
    current_step_index: int
    step_results: dict[str, StepResult]  # Typed results, not dict[str, Any]
    current_step_error: str

    # --- Written by VerifierNode ---
    verification: VerificationResult     # Proper model, not dict[str, Any]
    retry_count: int
    replan_count: int                    # Explicit counter (fixes Problem 9)
    total_node_calls: int

    # --- Written by OutputFormatterNode ---
    raw_analysis: str
    structured_output: dict[str, Any]    # LLM-generated JSON, shape varies
    typescript_component: dict[str, Any] # LLM-generated, shape varies

    # --- Shared ---
    error: str
    messages: list[str]


# =============================================================================
# Default State Factory
# =============================================================================


def create_initial_state(query: str) -> FinanceState:
    """
    Create a fresh FinanceState with sensible defaults for a new query.

    Args:
        query: The user's natural language question.

    Returns:
        A FinanceState dict ready to be passed to graph.invoke().
    """
    return FinanceState(
        query=query,
        query_type=QueryType.UNKNOWN,
        direct_response="",
        steps=[],
        decomposition_reasoning="",
        detected_tickers=[],
        current_step_index=0,
        step_results={},
        current_step_error="",
        verification=VerificationResult(verdict=Verdict.OK),
        retry_count=0,
        replan_count=0,
        total_node_calls=0,
        raw_analysis="",
        structured_output={},
        typescript_component={},
        error="",
        messages=[],
    )
