from __future__ import annotations

from kasparro_agentic.models import Product, ProductHighlights


def normalize_product(product: Product) -> Product:
    """
    Deterministic normalization: trims strings and ensures consistent types.
    No external data. No randomness.
    """
    return Product(
        product_name=product.product_name.strip(),
        brand=product.brand.strip(),
        category=product.category.strip(),
        price_inr=int(product.price_inr),
        key_ingredients=tuple(x.strip() for x in product.key_ingredients if x.strip()),
        benefits=tuple(x.strip() for x in product.benefits if x.strip()),
        skin_type=tuple(x.strip() for x in product.skin_type if x.strip()),
        concentration=product.concentration.strip(),
        how_to_use=product.how_to_use.strip(),
        side_effects=product.side_effects.strip(),
    )


def one_liner_summary(product: Product) -> str:
    ki = ", ".join(list(product.key_ingredients)[:3]) if product.key_ingredients else "key ingredients"
    st = ", ".join(product.skin_type) if product.skin_type else "most skin types"
    return f"{product.product_name} by {product.brand} is a {product.category.lower()} product for {st}, featuring {ki}."


def usage_block(product: Product) -> str:
    return product.how_to_use


def safety_block(product: Product) -> str:
    # Dataset-only. No medical claims.
    if product.side_effects.strip():
        return product.side_effects
    return "Patch test when trying new skincare. Discontinue use if irritation persists."


def product_page_highlights(product: Product) -> ProductHighlights:
    best_for = ", ".join(product.skin_type) if product.skin_type else "Not specified"
    return ProductHighlights(
        best_for=best_for,
        key_ingredients=list(product.key_ingredients),
        benefits=list(product.benefits),
        skin_types=list(product.skin_type),
    )


def compare_price(product_a: Product, product_b: Product) -> str:
    if product_a.price_inr == product_b.price_inr:
        return f"Both are priced at ₹{product_a.price_inr}."
    cheaper = product_a if product_a.price_inr < product_b.price_inr else product_b
    costlier = product_b if cheaper is product_a else product_a
    return f"{cheaper.product_name} is cheaper at ₹{cheaper.price_inr}, while {costlier.product_name} costs ₹{costlier.price_inr}."


def compare_ingredient_sets(product_a: Product, product_b: Product) -> str:
    a = set(product_a.key_ingredients)
    b = set(product_b.key_ingredients)
    both = sorted(a & b)
    only_a = sorted(a - b)
    only_b = sorted(b - a)

    parts: list[str] = []
    if both:
        parts.append(f"Both include: {', '.join(both)}.")
    if only_a:
        parts.append(f"Only {product_a.product_name} includes: {', '.join(only_a)}.")
    if only_b:
        parts.append(f"Only {product_b.product_name} includes: {', '.join(only_b)}.")
    return " ".join(parts) if parts else "Ingredient information is limited in the provided dataset."


def compare_benefits(product_a: Product, product_b: Product) -> str:
    a = set(product_a.benefits)
    b = set(product_b.benefits)
    both = sorted(a & b)
    only_a = sorted(a - b)
    only_b = sorted(b - a)

    parts: list[str] = []
    if both:
        parts.append(f"Both claim: {', '.join(both)}.")
    if only_a:
        parts.append(f"Only {product_a.product_name} claims: {', '.join(only_a)}.")
    if only_b:
        parts.append(f"Only {product_b.product_name} claims: {', '.join(only_b)}.")
    return " ".join(parts) if parts else "Benefits are limited in the provided dataset."


def disclaimer_informational() -> str:
    return "Informational only. Not medical advice. Patch test when trying new skincare."


def disclaimer_fictional_product() -> str:
    return "Note: Product B is fictional and generated for comparison purposes only."
