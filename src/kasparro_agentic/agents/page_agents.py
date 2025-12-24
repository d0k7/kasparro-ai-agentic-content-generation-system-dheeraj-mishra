from __future__ import annotations

from ..core.validation import (
    require,
    validate_comparison_page,
    validate_faq_page,
    validate_product_page,
)
from ..models import PipelineState
from ..templates.registry import DEFAULT_REGISTRY
from .base import Agent


class FAQPageAgent(Agent[PipelineState]):
    @property
    def name(self) -> str:
        return "faq_page_builder"

    def run(self, state: PipelineState) -> PipelineState:
        require(state.product is not None, "FAQPageAgent: product missing (run parser first).")
        require(state.questions is not None, "FAQPageAgent: questions missing (run question generator first).")

        payload = DEFAULT_REGISTRY.get("faq").render(state)
        validate_faq_page(payload)

        state.faq_page = payload
        return state


class ProductPageAgent(Agent[PipelineState]):
    @property
    def name(self) -> str:
        return "product_page_builder"

    def run(self, state: PipelineState) -> PipelineState:
        require(state.product is not None, "ProductPageAgent: product missing (run parser first).")

        payload = DEFAULT_REGISTRY.get("product_page").render(state)
        validate_product_page(payload)

        state.product_page = payload
        return state


class ComparisonPageAgent(Agent[PipelineState]):
    @property
    def name(self) -> str:
        return "comparison_page_builder"

    def run(self, state: PipelineState) -> PipelineState:
        require(state.product is not None, "ComparisonPageAgent: product missing (run parser first).")

        payload = DEFAULT_REGISTRY.get("comparison_page").render(state)
        validate_comparison_page(payload)

        state.comparison_page = payload
        return state
