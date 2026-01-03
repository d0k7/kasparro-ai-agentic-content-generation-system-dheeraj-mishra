# src/kasparro_agentic/core/validation.py
from __future__ import annotations


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)
