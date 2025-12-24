from __future__ import annotations

from ..models import FictionalProduct, Product


def build_product_b() -> FictionalProduct:
    """
    Produces a structured fictional Product B (explicitly allowed).
    """
    return FictionalProduct.build_default()


def build_comparison(product_a: Product, product_b: FictionalProduct) -> dict[str, object]:
    """
    Structured comparison (no external judgments; only simple deltas).
    """
    a_ing = set(product_a.key_ingredients)
    b_ing = set(product_b.key_ingredients)

    return {
        "shared": {
            "price_note": "Both are priced in INR (value depends on preferences and tolerance).",
            "format_note": "Both are serums.",
        },
        "differences": {
            "ingredients": {
                "product_a_only": sorted(a_ing - b_ing),
                "product_b_only": sorted(b_ing - a_ing),
                "shared": sorted(a_ing & b_ing),
            },
            "benefits": {
                "product_a": list(product_a.benefits),
                "product_b": list(product_b.benefits),
            },
            "price_inr": {
                "product_a": product_a.price_inr,
                "product_b": product_b.price_inr,
                "delta_b_minus_a": product_b.price_inr - product_a.price_inr,
            },
        },
        "selection_guide": [
            "Choose based on which ingredient set you prefer and what benefits you prioritize.",
            "If you have sensitive skin, introduce new actives gradually and monitor tolerance.",
        ],
    }
