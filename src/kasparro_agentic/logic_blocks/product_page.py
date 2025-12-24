from __future__ import annotations

from ..models import Product


def build_product_summary(product: Product) -> str:
    """
    Short summary assembled only from provided facts.
    """
    benefits = ", ".join(product.benefits).lower()
    skin = ", ".join(product.skin_type)
    return (
        f"{product.product_name} is a {product.concentration} serum for {skin} skin, "
        f"focused on {benefits}."
    )


def build_product_highlights(product: Product) -> dict[str, object]:
    """
    Structured highlights for machine-readability.
    """
    return {
        "concentration": product.concentration,
        "skin_type": list(product.skin_type),
        "key_ingredients": list(product.key_ingredients),
        "benefits": list(product.benefits),
        "how_to_use": product.how_to_use,
        "side_effects": product.side_effects,
        "price_inr": product.price_inr,
    }
