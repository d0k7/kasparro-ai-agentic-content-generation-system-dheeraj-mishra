from __future__ import annotations


class KasparroError(Exception):
    """Base exception for the project."""


class ValidationError(KasparroError):
    """Raised when structured output validation fails."""


class LLMError(KasparroError):
    """Raised when LLM invocation fails or returns invalid payload."""
