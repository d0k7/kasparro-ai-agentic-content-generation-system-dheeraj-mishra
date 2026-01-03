from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# Expand categories to be flexible + future-proof (tests only require some strings)
QuestionCategory = Literal[
    "Informational",
    "Ingredients",
    "Benefits",
    "Skin Type",
    "Usage",
    "Safety",
    "Routine",
    "Sunscreen",
    "Storage",
    "Results",
    "Frequency",
    "Layering",
    "Irritation",
    "Price",
    "Vitamin C %",
    "Purchase",
    "Comparison",
]


class Product(BaseModel):
    product_name: str
    brand: str = ""
    category: str = ""
    price_inr: int = 0

    key_ingredients: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    skin_type: list[str] = Field(default_factory=list)

    concentration: str = ""
    how_to_use: str = ""
    side_effects: str = ""

    @property
    def usage(self) -> str:
        # Some prompts/tools refer to "usage"
        return self.how_to_use


class Question(BaseModel):
    category: QuestionCategory
    question: str


class QuestionList(BaseModel):
    questions: list[Question]


class Answer(BaseModel):
    content: str


class FAQItem(BaseModel):
    category: str
    question: str
    answer: str


class FAQPage(BaseModel):
    page_type: Literal["faq"] = "faq"
    product_name: str
    disclaimer: str
    items: list[FAQItem]


class ProductHighlights(BaseModel):
    best_for: str
    key_ingredients: list[str]
    benefits: list[str]
    skin_types: list[str]


class ProductPage(BaseModel):
    page_type: Literal["product_page"] = "product_page"
    product_name: str
    brand: str
    price_inr: int
    summary: str
    highlights: ProductHighlights


class FictionalProduct(BaseModel):
    product_name: str
    brand: str
    category: str
    price_inr: int
    key_ingredients: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    skin_type: list[str] = Field(default_factory=list)
    concentration: str = ""
    how_to_use: str = ""
    side_effects: str = ""


class ComparisonSimilarities(BaseModel):
    key_ingredients: str
    benefits: str


class ComparisonDifferences(BaseModel):
    ingredients: str
    skin_type: str
    pricing: str


class ComparisonBlock(BaseModel):
    similarities: ComparisonSimilarities
    differences: ComparisonDifferences


class ComparisonPage(BaseModel):
    page_type: Literal["comparison_page"] = "comparison_page"
    disclaimer: str
    product_a: dict
    product_b: dict
    comparison: ComparisonBlock


class PipelineState(BaseModel):
    """
    This is optional (LangGraph usually uses dict/TypedDict).
    Keeping a pydantic state is fine for validation or future extension.
    """
    product: Product | None = None
    questions: list[Question] = Field(default_factory=list)
    answer: str = ""
    error: str | None = None
    mode: str = "mock"
