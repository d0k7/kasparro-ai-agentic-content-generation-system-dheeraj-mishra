from __future__ import annotations

from kasparro_agentic.llm.provider import LLMProvider
from kasparro_agentic.logic_blocks.blocks import one_liner_summary, product_page_highlights
from kasparro_agentic.models import Product, ProductPage


def _product_page_prompt(product: Product) -> str:
    return f"""
You are generating a structured product page JSON using ONLY the given dataset fields.
Do NOT invent new facts.

Product:
- product_name: {product.product_name}
- brand: {product.brand}
- category: {product.category}
- price_inr: {product.price_inr}
- key_ingredients: {list(product.key_ingredients)}
- benefits: {list(product.benefits)}
- skin_type: {list(product.skin_type)}
- concentration: {product.concentration}
- how_to_use: {product.how_to_use}
- side_effects: {product.side_effects}

Return JSON matching the ProductPage schema.
""".strip()


def build_product_page(product: Product, llm: LLMProvider) -> ProductPage:
    page = llm.invoke_structured(_product_page_prompt(product), ProductPage)

    # Guardrail: keep highlights/summary dataset-consistent even if LLM deviates
    page.summary = one_liner_summary(product)
    page.highlights = product_page_highlights(product)
    return page
