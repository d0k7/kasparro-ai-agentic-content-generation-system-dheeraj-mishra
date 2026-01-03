# src/kasparro_agentic/templates/base.py
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

TOut = TypeVar("TOut", bound=BaseModel)


class Template(ABC, Generic[TOut]):
    """
    Template Engine primitive:
      - schema: the exact structured output model
      - dependencies: which logic blocks it relies on (documented + testable)
      - build_context(): collects data for the prompt (data → blocks → context)
      - build_prompt(): formatting + rules + JSON schema instructions
    """

    name: str
    schema: type[TOut]
    dependencies: tuple[str, ...]

    @abstractmethod
    def build_context(self, **kwargs: object) -> dict[str, object]:
        raise NotImplementedError

    def build_prompt(self, context: dict[str, object]) -> str:
        # Standardized context framing so the mock provider can deterministically parse inputs
        context_json = json.dumps(context, ensure_ascii=False, indent=2)
        return "\n".join(
            [
                "You are an expert content generator.",
                "Use ONLY the provided context. Do not add external facts.",
                "Return ONLY valid JSON that matches the required schema exactly.",
                "",
                "<<<CONTEXT_JSON>>>",
                context_json,
                "<<<END_CONTEXT_JSON>>>",
                "",
                "JSON ONLY. No markdown. No commentary.",
            ]
        )
