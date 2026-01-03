from __future__ import annotations

from kasparro_agentic.llm.provider import build_llm_provider
from kasparro_agentic.models import Product, Question, QuestionList


def generate_questions(product: Product) -> list[Question]:
    llm = build_llm_provider()

    prompt = f"""
Generate at least 15 product FAQ questions with categories.
Return JSON matching this schema:

{{
  "questions": [
    {{"category": "Benefits", "question": "..."}},
    ...
  ]
}}

Product context:
- product_name: {product.product_name}
- brand: {product.brand}
- category: {product.category}
- benefits: {product.benefits}
- how_to_use: {product.how_to_use}
""".strip()

    out = llm.invoke_structured(prompt, QuestionList)
    return out.questions


def generate_answer(product: Product, question: str) -> str:
    llm = build_llm_provider()

    prompt = f"""
You are an expert product assistant.
Write a clear, helpful, safe, non-medical answer to the question below,
based on the provided product context.

Question: {question}

Product Context:
- Name: {product.product_name}
- Brand: {product.brand}
- Key Ingredients: {product.key_ingredients}
- How to use: {product.how_to_use}
- Side effects: {product.side_effects}

Constraints:
- Be practical and consumer-friendly.
- Mention patch test and irritation guidance.
- Avoid medical claims.
""".strip()

    return llm.invoke_text(prompt).strip()
