from __future__ import annotations

from ..core.validation import require, require_not_none
from ..models import PipelineState, Question
from .base import Agent


class QuestionGenerationAgent(Agent[PipelineState]):
    """Generates >=15 categorized user questions deterministically from the product model."""

    @property
    def name(self) -> str:
        return "question_generator"

    def run(self, state: PipelineState) -> PipelineState:
        p = require_not_none(state.product, "QuestionGenerationAgent: product missing (run parser first).")

        skin = ", ".join(p.skin_type)
        benefits = ", ".join(p.benefits)
        ingredients = ", ".join(p.key_ingredients)

        questions: list[Question] = [
            # Informational
            Question("Informational", f"What is {p.product_name}?"),
            Question("Informational", f"What is the concentration of Vitamin C in {p.product_name}?"),
            Question("Informational", f"Which skin types is {p.product_name} meant for?"),
            Question("Informational", f"What are the key ingredients in {p.product_name}?"),
            Question("Informational", f"What benefits does {p.product_name} claim? ({benefits})"),

            # Usage
            Question("Usage", f"How do I use {p.product_name} in a morning routine?"),
            Question("Usage", f"How many drops of {p.product_name} should I apply?"),
            Question("Usage", f"When should I apply sunscreen if I use {p.product_name}?"),
            Question("Usage", f"Can {p.product_name} be used daily for {skin} skin?"),

            # Safety
            Question("Safety", f"Are there any side effects from using {p.product_name}?"),
            Question("Safety", f"What should sensitive skin users know before trying {p.product_name}?"),
            Question("Safety", f"What does mild tingling mean when using {p.product_name}?"),

            # Purchase
            Question("Purchase", f"What is the price of {p.product_name}?"),
            Question("Purchase", f"Is ₹{p.price_inr} reasonable given its ingredients ({ingredients})?"),

            # Comparison
            Question("Comparison", f"How does {p.product_name} compare to another serum with different actives?"),
            Question("Comparison", f"What should I compare when choosing between {p.product_name} and a different serum?"),
        ]

        require(len(questions) >= 15, "QuestionGenerationAgent must generate at least 15 questions.")
        state.questions = questions
        return state
