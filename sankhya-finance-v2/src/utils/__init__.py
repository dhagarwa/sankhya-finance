"""
Utilities - Shared helpers used across the entire application.

Contains:
    - model_config: Centralized OpenAI model selection and configuration.
      All nodes use get_llm() from here -- no duplicated model logic.
"""

from .model_config import get_llm

__all__ = ["get_llm"]
