from __future__ import annotations

from kasparro_agentic.llm.provider import LLMProvider
from kasparro_agentic.logic_blocks.blocks import disclaimer_informational, safety_block, usage_block
from kasparro_agentic.models import FAQItem, FAQPage, Product, Question


def _faq_prompt(product: Product, questions: list[Question]) -> str:
    return f"""
You are generating a FAQPage JSON using ONLY the given dataset fields.
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

Questions:
{[q.model_dump() for q in questions]}

Return JSON matching the FAQPage schema.
""".strip()


def build_faq_page(product: Product, questions: list[Question], llm: LLMProvider) -> FAQPage:
    page = llm.invoke_structured(_faq_prompt(product, questions), FAQPage)
    page.disclaimer = disclaimer_informational()

    # Deterministic fallback if LLM returns too few items
    if len(page.items) < 15:
        items: list[FAQItem] = []
        for q in questions:
            if q.category == "Usage":
                ans = usage_block(product)
            elif q.category == "Safety":
                ans = safety_block(product)
            elif q.category == "Price":
                ans = f"The listed price is ₹{product.price_inr}."
            elif q.category == "Vitamin C %":
                ans = f"Concentration: {product.concentration}."
            else:
                ans = "This information is not specified in the provided dataset."
            items.append(FAQItem(category=q.category, question=q.question, answer=ans))
        page.items = items[:15]

    return page
