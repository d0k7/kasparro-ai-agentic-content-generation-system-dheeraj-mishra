from __future__ import annotations

from typing import Any, Literal, TypeAlias

from pydantic import BaseModel, Field

# ----------------------------
# Core domain models
# ----------------------------

class Product(BaseModel):
    product_name: str
    brand: str
    category: str
    price_inr: int

    # Keep tuples for immutability + deterministic ordering in JSON dumps if you sort upstream.
    key_ingredients: tuple[str, ...] = Field(default_factory=tuple)
    benefits: tuple[str, ...] = Field(default_factory=tuple)
    skin_type: tuple[str, ...] = Field(default_factory=tuple)

    # Required by your existing pipeline and blocks.py
    concentration: str = "Not specified in the provided dataset."
    how_to_use: str = "Not specified in the provided dataset."

    # Force non-optional because your blocks.py expects str
    side_effects: str = "Not specified in the provided dataset."


class FictionalProduct(Product):
    """Competitor product synthesized by an agent or deterministic logic."""
    pass


# ----------------------------
# Question models
# ----------------------------

QuestionCategory: TypeAlias = Literal[
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
]


class Question(BaseModel):
    category: QuestionCategory
    question: str


class QuestionList(BaseModel):
    questions: list[Question]


# ----------------------------
# FAQ page models
# ----------------------------

class FAQItem(BaseModel):
    category: str
    question: str
    answer: str


class FAQPage(BaseModel):
    page_type: Literal["faq"] = "faq"
    product_name: str
    disclaimer: str
    items: list[FAQItem]


# ----------------------------
# Product page models
# ----------------------------

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


# ----------------------------
# Comparison page models
# ----------------------------

class ComparisonProductBlock(BaseModel):
    product_name: str
    price_inr: int
    key_ingredients: list[str]
    benefits: list[str]
    skin_type: list[str]


class ComparisonSimilarities(BaseModel):
    key_ingredients: str
    benefits: str


class ComparisonDifferences(BaseModel):
    ingredients: str
    skin_type: str
    pricing: str


class ComparisonSection(BaseModel):
    similarities: ComparisonSimilarities
    differences: ComparisonDifferences


class ComparisonPage(BaseModel):
    page_type: Literal["comparison_page"] = "comparison_page"
    disclaimer: str
    product_a: ComparisonProductBlock
    product_b: ComparisonProductBlock
    comparison: ComparisonSection


# ----------------------------
# PipelineState (used by templates/tooling)
# ----------------------------

class PipelineState(BaseModel):
    product: Product | None = None
    questions: list[Question] = Field(default_factory=list)
    faq: FAQPage | None = None
    product_page: ProductPage | None = None
    fictional_product_b: FictionalProduct | None = None
    comparison_page: ComparisonPage | None = None
    dag_metadata: dict[str, Any] | None = None
# ----------------------------
# Answer models (Added to fix ImportError)
# ----------------------------

class Answer(BaseModel):
    """Schema for a single structured FAQ answer."""
    question: str = Field(description="The original customer question")
    answer: str = Field(description="The helpful, concise, and safe answer")
    category: str = Field(description="The category this FAQ belongs to")
    safety_disclaimer: str = Field(
        default="Consult a dermatologist before starting new active ingredients.",
        description="Standard safety advice for skincare products"
    )