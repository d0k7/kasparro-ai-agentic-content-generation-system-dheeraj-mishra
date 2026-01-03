from __future__ import annotations

from kasparro_agentic.llm.provider import LLMProvider
from kasparro_agentic.models import ComparisonPage, FictionalProduct, Product


def _comparison_prompt(product_a: Product, product_b: FictionalProduct) -> str:
    return f"""
You are generating a comparison page as strict JSON matching the provided schema.

RULES:
- Product B is fictional, but must still be coherent.
- Use only provided product fields for A and B.
- No external claims.
- Similarities and differences must reference ingredient/benefit/skin_type/price.

PRODUCT A:
- product_name: {product_a.product_name}
- brand: {product_a.brand}
- price_inr: {product_a.price_inr}
- key_ingredients: {list(product_a.key_ingredients)}
- benefits: {list(product_a.benefits)}
- skin_type: {list(product_a.skin_type)}

PRODUCT B (fictional):
- product_name: {product_b.product_name}
- brand: {product_b.brand}
- price_inr: {product_b.price_inr}
- key_ingredients: {list(product_b.key_ingredients)}
- benefits: {list(product_b.benefits)}
- skin_type: {list(product_b.skin_type)}
""".strip()


def build_comparison_page(product_a: Product, product_b: FictionalProduct, llm: LLMProvider) -> ComparisonPage:
    return llm.invoke_structured(_comparison_prompt(product_a, product_b), ComparisonPage)
