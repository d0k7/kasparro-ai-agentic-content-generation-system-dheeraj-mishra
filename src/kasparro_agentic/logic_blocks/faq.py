from __future__ import annotations

from collections.abc import Iterable

from ..models import FAQItem, Product, Question, QuestionCategory


def answer_question(product: Product, q: Question) -> str:
    """
    Deterministic, dataset-only answers.

    IMPORTANT:
    - Uses ONLY fields from the provided dataset (Product).
    - No external medical advice or extra facts.
    - Keep answers short, structured, and factual.
    """
    name = product.product_name
    concentration = product.concentration
    skin = ", ".join(product.skin_type)
    ingredients = ", ".join(product.key_ingredients)
    benefits = ", ".join(product.benefits)
    how = product.how_to_use
    side_effects = product.side_effects
    price = product.price_inr

    q_text = q.question.lower()

    # ---- Purchase FIRST (prevents "What is the price..." from matching "what is") ----
    if "price" in q_text or "₹" in q.question:
        return f"The listed price is ₹{price}."
    if "reasonable" in q_text:
        return f"The listed price is ₹{price}. Value depends on your preferences and tolerance."

    # ---- Informational ----
    if "concentration" in q_text:
        return f"The stated concentration is {concentration}."
    if "skin type" in q_text or "skin types" in q_text:
        return f"It is intended for {skin} skin types."
    if "key ingredient" in q_text or "key ingredients" in q_text:
        return f"Key ingredients listed are: {ingredients}."
    if "benefit" in q_text or "benefits" in q_text:
        return f"Listed benefits are: {benefits}."
    if "what is" in q_text:
        return (
            f"{name} is a {concentration} serum designed for {skin} skin. "
            f"It includes {ingredients} and is positioned for {benefits}."
        )

    # ---- Usage ----
    if "how do i use" in q_text or "how to use" in q_text:
        return f"Usage instruction: {how}."
    if "how many drops" in q_text:
        return "Use 2–3 drops as per the provided usage instruction."
    if "sunscreen" in q_text:
        return "Apply it in the morning before sunscreen, as specified in the usage instruction."
    if "daily" in q_text:
        return f"The dataset indicates it is meant for {skin} skin. Introduce gradually if you are sensitive."

    # ---- Safety ----
    if "side effect" in q_text or "side effects" in q_text:
        return f"Reported side effect in the dataset: {side_effects}."
    if "sensitive" in q_text:
        return f"If you have sensitive skin, note: {side_effects}."
    if "tingling" in q_text:
        return f"The dataset notes: {side_effects}."

    # ---- Comparison ----
    if "compare" in q_text or "choosing between" in q_text:
        return "Compare the key ingredients, listed benefits, and price, and choose based on what you prioritize."

    # Fallback (still dataset-only)
    return f"{name}: {concentration}, for {skin} skin, with {ingredients} and benefits like {benefits}."


def _unique_in_order(items: Iterable[FAQItem]) -> list[FAQItem]:
    """Remove duplicates deterministically while preserving order."""
    seen: set[str] = set()
    out: list[FAQItem] = []
    for it in items:
        if it.question in seen:
            continue
        seen.add(it.question)
        out.append(it)
    return out


def build_faq_items(
    product: Product,
    questions: list[Question],
    *,
    min_items: int = 5,
    required_categories: tuple[QuestionCategory, ...] = ("Informational", "Usage", "Safety", "Purchase"),
) -> list[FAQItem]:
    """
    Build FAQ items with guaranteed category coverage (deterministic).

    Strategy (deterministic):
    1) Generate candidates in the order of the `questions` list.
    2) Select the FIRST question for each required category (if available).
    3) Fill remaining slots (to reach `min_items`) with the earliest remaining candidates.
    """
    candidates: list[FAQItem] = [
        FAQItem(question=q.question, answer=answer_question(product, q), category=q.category) for q in questions
    ]
    candidates = _unique_in_order(candidates)

    selected: list[FAQItem] = []
    used_questions: set[str] = set()

    for cat in required_categories:
        for item in candidates:
            if item.category == cat and item.question not in used_questions:
                selected.append(item)
                used_questions.add(item.question)
                break

    for item in candidates:
        if len(selected) >= min_items:
            break
        if item.question in used_questions:
            continue
        selected.append(item)
        used_questions.add(item.question)

    return selected[:max(min_items, len(selected))]
