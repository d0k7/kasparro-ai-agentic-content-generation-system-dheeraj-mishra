from __future__ import annotations

from dataclasses import dataclass

from kasparro_agentic.templates.pages import (
    ComparisonPageTemplate,
    FAQTemplate,
    ProductPageTemplate,
    QuestionTemplate,
)


@dataclass(frozen=True)
class TemplateRegistry:
    """
    Central place to access template implementations.
    This keeps the codebase modular and makes swapping templates easy.
    """
    question: QuestionTemplate
    faq: FAQTemplate
    product_page: ProductPageTemplate
    comparison_page: ComparisonPageTemplate


def build_registry() -> TemplateRegistry:
    return TemplateRegistry(
        question=QuestionTemplate(),
        faq=FAQTemplate(),
        product_page=ProductPageTemplate(),
        comparison_page=ComparisonPageTemplate(),
    )
