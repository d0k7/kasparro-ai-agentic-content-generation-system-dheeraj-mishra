from __future__ import annotations

from kasparro_agentic.models import FictionalProduct, Product


def build_fictional_product_b(product_a: Product) -> FictionalProduct:
    return FictionalProduct(
        product_name=f"{product_a.brand} Radiance C+ Serum",
        brand=f"{product_a.brand} Labs",
        category=product_a.category,
        price_inr=max(499, product_a.price_inr + 200),
        key_ingredients=(
            "8% Vitamin C",
            "Ferulic Acid",
            "Vitamin E",
        ),
        benefits=(
            "Brightening",
            "Helps reduce dullness",
            "Antioxidant support",
        ),
        skin_type=(
            "Normal",
            "Combination",
        ),
        concentration="8% Vitamin C",
        how_to_use="Apply 2–3 drops on clean face in the morning. Follow with moisturizer and sunscreen.",
        side_effects="Not specified in the provided dataset.",
    )
