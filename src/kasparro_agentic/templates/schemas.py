from __future__ import annotations

from pydantic import BaseModel, Field


class QuestionListSchema(BaseModel):
    questions: list[dict] = Field(default_factory=list, description="List of {category, question}")


class FAQPageSchema(BaseModel):
    page_type: str = "faq"
    product_name: str
    disclaimer: str
    items: list[dict]


class ProductPageSchema(BaseModel):
    page_type: str = "product_page"
    product_name: str
    brand: str
    price_inr: int
    summary: str
    highlights: list[str]


class ComparisonPageSchema(BaseModel):
    page_type: str = "comparison_page"
    product_a: dict
    product_b: dict
    comparison_points: list[dict]
