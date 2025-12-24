from __future__ import annotations

from typing import Any, TypeVar

from .errors import ValidationError

T = TypeVar("T")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def require_not_none(value: T | None, message: str) -> T:
    """
    Runtime check + mypy type narrowing.
    Use this instead of require(x is not None, ...) when you want mypy to understand.
    """
    if value is None:
        raise ValidationError(message)
    return value


def require_keys(obj: dict[str, Any], keys: list[str], context: str) -> None:
    missing = [k for k in keys if k not in obj]
    require(not missing, f"{context}: missing keys: {missing}")


def require_type(value: Any, t: type, context: str) -> None:
    require(isinstance(value, t), f"{context}: expected {t.__name__}, got {type(value).__name__}")


def validate_faq_page(page: dict[str, Any]) -> None:
    require_keys(page, ["page_type", "product_name", "items", "disclaimer"], "FAQPage")
    require(page["page_type"] == "faq", "FAQPage: page_type must be 'faq'")
    require_type(page["product_name"], str, "FAQPage.product_name")
    require_type(page["disclaimer"], str, "FAQPage.disclaimer")

    items = page["items"]
    require_type(items, list, "FAQPage.items")
    require(len(items) >= 5, "FAQPage.items must have at least 5 Q&As")

    for i, item in enumerate(items):
        require_type(item, dict, f"FAQPage.items[{i}]")
        require_keys(item, ["question", "answer", "category"], f"FAQPage.items[{i}]")
        require_type(item["question"], str, f"FAQPage.items[{i}].question")
        require_type(item["answer"], str, f"FAQPage.items[{i}].answer")
        require_type(item["category"], str, f"FAQPage.items[{i}].category")


def validate_product_page(page: dict[str, Any]) -> None:
    require_keys(page, ["page_type", "product_name", "summary", "highlights", "disclaimer"], "ProductPage")
    require(page["page_type"] == "product_page", "ProductPage: page_type must be 'product_page'")
    require_type(page["product_name"], str, "ProductPage.product_name")
    require_type(page["summary"], str, "ProductPage.summary")
    require_type(page["highlights"], dict, "ProductPage.highlights")
    require_type(page["disclaimer"], str, "ProductPage.disclaimer")


def validate_comparison_page(page: dict[str, Any]) -> None:
    require_keys(page, ["page_type", "product_a", "product_b", "comparison", "disclaimer"], "ComparisonPage")
    require(page["page_type"] == "comparison_page", "ComparisonPage: page_type must be 'comparison_page'")
    require_type(page["product_a"], dict, "ComparisonPage.product_a")
    require_type(page["product_b"], dict, "ComparisonPage.product_b")
    require_type(page["comparison"], dict, "ComparisonPage.comparison")
    require_type(page["disclaimer"], str, "ComparisonPage.disclaimer")
