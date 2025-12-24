from __future__ import annotations

from ..logic_blocks import (
    build_comparison,
    build_faq_items,
    build_product_b,
    build_product_highlights,
    build_product_summary,
)
from ..models import PipelineState
from .template_engine import Template, TemplateField

FAQ_DISCLAIMER = "Informational only. Not medical advice. Patch test when trying new skincare."
GENERIC_DISCLAIMER = "Informational only. This content is generated from a limited dataset."
COMPARISON_DISCLAIMER = "Product B is fictional. Informational only."


def _faq_items(state: PipelineState) -> object:
    assert state.product is not None
    assert state.questions is not None

    items = build_faq_items(state.product, state.questions, min_items=5)
    return [{"question": i.question, "answer": i.answer, "category": i.category} for i in items]


FAQ_TEMPLATE: Template[PipelineState] = Template(
    name="faq_template",
    fields=(
        TemplateField("page_type", lambda _: "faq"),
        TemplateField("product_name", lambda s: s.product.product_name if s.product else ""),
        TemplateField("items", _faq_items),
        TemplateField("disclaimer", lambda _: FAQ_DISCLAIMER),
    ),
)

PRODUCT_TEMPLATE: Template[PipelineState] = Template(
    name="product_template",
    fields=(
        TemplateField("page_type", lambda _: "product_page"),
        TemplateField("product_name", lambda s: s.product.product_name if s.product else ""),
        TemplateField("summary", lambda s: build_product_summary(s.product) if s.product else ""),
        TemplateField("highlights", lambda s: build_product_highlights(s.product) if s.product else {}),
        TemplateField("disclaimer", lambda _: GENERIC_DISCLAIMER),
    ),
)


def _ensure_product_b(state: PipelineState) -> None:
    if state.fictional_product_b is None:
        state.fictional_product_b = build_product_b()


def _comparison_payload(state: PipelineState) -> dict[str, object]:
    assert state.product is not None
    _ensure_product_b(state)
    assert state.fictional_product_b is not None

    a = state.product
    b = state.fictional_product_b

    return {
        "product_a": {
            "product_name": a.product_name,
            "key_ingredients": list(a.key_ingredients),
            "benefits": list(a.benefits),
            "price_inr": a.price_inr,
        },
        "product_b": {
            "product_name": b.product_name,
            "key_ingredients": list(b.key_ingredients),
            "benefits": list(b.benefits),
            "price_inr": b.price_inr,
        },
        "comparison": build_comparison(a, b),
    }


COMPARISON_TEMPLATE: Template[PipelineState] = Template(
    name="comparison_template",
    fields=(
        TemplateField("page_type", lambda _: "comparison_page"),
        TemplateField("product_a", lambda s: _comparison_payload(s)["product_a"]),
        TemplateField("product_b", lambda s: _comparison_payload(s)["product_b"]),
        TemplateField("comparison", lambda s: _comparison_payload(s)["comparison"]),
        TemplateField("disclaimer", lambda _: COMPARISON_DISCLAIMER),
    ),
)
