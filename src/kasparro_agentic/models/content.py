from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .product import FictionalProduct, Product

QuestionCategory = Literal["Informational", "Safety", "Usage", "Purchase", "Comparison"]


@dataclass(frozen=True, slots=True)
class Question:
    category: QuestionCategory
    question: str


@dataclass(frozen=True, slots=True)
class FAQItem:
    """
    Strongly-typed intermediate representation for FAQ items.
    Later rendered to JSON dicts via templates.
    """
    question: str
    answer: str
    category: QuestionCategory


@dataclass(slots=True)
class PipelineState:
    """
    Shared pipeline state passed between agents.

    - Explicitly passed between nodes (no hidden global state).
    - Validated at boundaries using core.validation helpers.
    """

    raw_product: dict[str, object]
    output_dir: Path

    # Orchestration visibility
    dag_metadata: dict[str, object] | None = None

    product: Product | None = None
    fictional_product_b: FictionalProduct | None = None
    questions: list[Question] | None = None

    # Final rendered pages (machine-readable dicts)
    faq_page: dict[str, object] | None = None
    product_page: dict[str, object] | None = None
    comparison_page: dict[str, object] | None = None
