from __future__ import annotations

from typing import Any

from kasparro_agentic.llm.provider import build_llm_provider
from kasparro_agentic.logic_blocks.comparison import build_fictional_product_b
from kasparro_agentic.logic_blocks.comparison_page import build_comparison_page
from kasparro_agentic.logic_blocks.faq import build_faq_page
from kasparro_agentic.logic_blocks.product_page import build_product_page
from kasparro_agentic.models import FictionalProduct, Product, Question


def build_faq_page_agent(product: Product, questions: list[Question]) -> dict[str, Any]:
    llm = build_llm_provider()
    page = build_faq_page(product=product, questions=questions, llm=llm)
    return page.model_dump()


def build_product_page_agent(product: Product) -> dict[str, Any]:
    llm = build_llm_provider()
    page = build_product_page(product=product, llm=llm)
    return page.model_dump()


def build_fictional_product_b_agent(product_a: Product) -> FictionalProduct:
    # This is intentionally separated: competitor generation is its own "agentic" step.
    return build_fictional_product_b(product_a)


def build_comparison_page_agent(product_a: Product, product_b: FictionalProduct) -> dict[str, Any]:
    llm = build_llm_provider()
    page = build_comparison_page(product_a=product_a, product_b=product_b, llm=llm)
    return page.model_dump()
