"""
Centralized OpenAI Model Configuration.

This is the SINGLE place where LLM model selection happens in the entire
application. Every node calls get_llm() instead of managing its own
client/model/fallback logic.

Why this matters:
    In v1, three separate classes each had their own _get_best_model() and
    _create_chat_completion() methods, and DataRetrievalAgent had yet another
    hardcoded fallback. Now there's just one function.

Usage:
    from src.utils.model_config import get_llm

    llm = get_llm()                          # Default: gpt-4o, temp=0.1
    llm = get_llm(temperature=0)             # Override temperature
    llm = get_llm(model="gpt-4o-mini")       # Use a specific model
"""

import os
from functools import lru_cache

from langchain_openai import ChatOpenAI


# =============================================================================
# Model Priority List
# =============================================================================
# When no specific model is requested, we use the first available model
# from this list. gpt-4o is the default -- reliable, fast, and widely
# available. gpt-5 can be added when it becomes generally available.
# =============================================================================

DEFAULT_MODEL = "gpt-4o"

# Models we support, in order of preference
SUPPORTED_MODELS = [
    "gpt-4o",               # Default: good balance of speed and quality
    "gpt-4o-mini",          # Cheaper/faster for simple tasks
    "gpt-4-turbo",          # Fallback if gpt-4o unavailable
]


def get_llm(
    *,
    model: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    streaming: bool = False,
) -> ChatOpenAI:
    """
    Get a configured ChatOpenAI instance.

    This is the ONE function every node in the graph calls to get an LLM.
    No node should ever create its own OpenAI client directly.

    Args:
        model:       Which OpenAI model to use. Defaults to gpt-4o.
        temperature: Sampling temperature (0 = deterministic, 1 = creative).
                     Default 0.1 for financial analysis (we want consistency).
        max_tokens:  Maximum tokens in the response. Default 4096.
        streaming:   Whether to enable streaming mode. Default False.

    Returns:
        A configured ChatOpenAI instance ready for .invoke() or .ainvoke().

    Raises:
        ValueError: If OPENAI_API_KEY is not set in environment.

    Example:
        >>> llm = get_llm()
        >>> response = await llm.ainvoke([HumanMessage(content="Hello")])
    """
    # --- Resolve API key ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your-"):
        raise ValueError(
            "OPENAI_API_KEY not configured. "
            "Copy .env.template to .env and add your key."
        )

    # --- Resolve model ---
    selected_model = model or DEFAULT_MODEL

    # --- Build and return the LLM ---
    return ChatOpenAI(
        model=selected_model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=streaming,
    )


def get_api_key() -> str:
    """
    Get the OpenAI API key from the environment.

    Utility function for cases where we need the raw key
    (e.g., for direct OpenAI SDK calls in ticker extraction).

    Returns:
        The API key string.

    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("your-"):
        raise ValueError(
            "OPENAI_API_KEY not configured. "
            "Copy .env.template to .env and add your key."
        )
    return api_key
