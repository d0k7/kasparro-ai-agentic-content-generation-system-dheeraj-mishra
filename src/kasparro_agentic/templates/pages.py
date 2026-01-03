from __future__ import annotations

from dataclasses import dataclass

from kasparro_agentic.logic_blocks.blocks import (
    compare_benefits,
    compare_ingredient_sets,
    compare_price,
    disclaimer_fictional_product,
    disclaimer_informational,
    normalize_product,
    one_liner_summary,
    product_page_highlights,
    safety_block,
    usage_block,
)
from kasparro_agentic.models import (
    ComparisonDifferences,
    ComparisonPage,
    ComparisonProductBlock,
    ComparisonSection,
    ComparisonSimilarities,
    FAQItem,
    FAQPage,
    FictionalProduct,
    Product,
    ProductPage,
    Question,
)


def render_faq_page(product: Product, questions: list[Question]) -> FAQPage:
    p = normalize_product(product)

    items: list[FAQItem] = []
    for q in questions:
        if q.category == "Usage":
            ans = usage_block(p)
        elif q.category == "Safety":
            ans = safety_block(p)
        elif q.category == "Price":
            ans = f"The listed price is ₹{p.price_inr}."
        elif q.category == "Vitamin C %":
            ans = f"Concentration: {p.concentration}."
        else:
            ans = "This information is not specified in the provided dataset."

        items.append(FAQItem(category=q.category, question=q.question, answer=ans))

    return FAQPage(
        product_name=p.product_name,
        disclaimer=disclaimer_informational(),
        items=items[:15],
    )


def render_product_page(product: Product) -> ProductPage:
    p = normalize_product(product)
    return ProductPage(
        product_name=p.product_name,
        brand=p.brand,
        price_inr=p.price_inr,
        summary=one_liner_summary(p),
        highlights=product_page_highlights(p),
    )


def render_comparison_page(product_a: Product, product_b: FictionalProduct) -> ComparisonPage:
    a = normalize_product(product_a)
    b = normalize_product(product_b)

    a_block = ComparisonProductBlock(
        product_name=a.product_name,
        price_inr=a.price_inr,
        key_ingredients=list(a.key_ingredients),
        benefits=list(a.benefits),
        skin_type=list(a.skin_type),
    )
    b_block = ComparisonProductBlock(
        product_name=b.product_name,
        price_inr=b.price_inr,
        key_ingredients=list(b.key_ingredients),
        benefits=list(b.benefits),
        skin_type=list(b.skin_type),
    )

    similarities = ComparisonSimilarities(
        key_ingredients=compare_ingredient_sets(a, b),
        benefits=compare_benefits(a, b),
    )

    differences = ComparisonDifferences(
        ingredients=compare_ingredient_sets(a, b),
        skin_type=(
            f"{a.product_name} skin types: {', '.join(a.skin_type)}. "
            f"{b.product_name} skin types: {', '.join(b.skin_type)}."
        ),
        pricing=compare_price(a, b),
    )

    section = ComparisonSection(
        similarities=similarities,
        differences=differences,
    )

    return ComparisonPage(
        disclaimer=disclaimer_fictional_product(),
        product_a=a_block,
        product_b=b_block,
        comparison=section,
    )


# -------------------------------------------------------------------
# Template classes (registry.py expects these names)
# -------------------------------------------------------------------

@dataclass(frozen=True)
class QuestionTemplate:
    """
    Backwards-compat for registry imports.

    Note: agentic question generation is handled in agents/question_agent.py (LLM-based),
    but this template provides a safe deterministic fallback if used directly.
    """
    def render(self, product: Product) -> list[Question]:
        name = product.product_name
        return [
            Question(category="Informational", question=f"What is {name}?"),
            Question(category="Ingredients", question="What are the key ingredients?"),
            Question(category="Benefits", question="What benefits does it provide?"),
            Question(category="Skin Type", question="Is it suitable for my skin type?"),
            Question(category="Usage", question="How do I use it?"),
            Question(category="Safety", question="Are there any side effects or precautions?"),
            Question(category="Routine", question="Where does it fit in my routine?"),
            Question(category="Sunscreen", question="Do I need sunscreen after using it?"),
            Question(category="Storage", question="How should I store it?"),
            Question(category="Results", question="When can I expect results?"),
            Question(category="Frequency", question="How often should I use it?"),
            Question(category="Layering", question="Can I layer it with other actives?"),
            Question(category="Irritation", question="What if it causes irritation?"),
            Question(category="Price", question="What is the price?"),
            Question(category="Vitamin C %", question="What is the Vitamin C concentration?"),
        ]


@dataclass(frozen=True)
class FAQTemplate:
    def render(self, product: Product, questions: list[Question]) -> FAQPage:
        return render_faq_page(product, questions)


@dataclass(frozen=True)
class ProductPageTemplate:
    def render(self, product: Product) -> ProductPage:
        return render_product_page(product)


@dataclass(frozen=True)
class ComparisonPageTemplate:
    def render(self, product_a: Product, product_b: FictionalProduct) -> ComparisonPage:
        return render_comparison_page(product_a, product_b)
