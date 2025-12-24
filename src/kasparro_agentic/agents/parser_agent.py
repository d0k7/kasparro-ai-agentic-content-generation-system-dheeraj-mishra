from __future__ import annotations

from typing import Any, cast

from ..core.validation import require, require_keys
from ..models import PipelineState, Product
from .base import Agent


def _as_str_list(value: object, field_name: str) -> list[str]:
    """
    Convert an unknown object into list[str] with runtime validation.
    Written to satisfy mypy strict checks.
    """
    require(isinstance(value, list), f"{field_name} must be a list")

    # After runtime check, cast for static typing.
    items = cast(list[object], value)

    out: list[str] = []
    for i, item in enumerate(items):
        require(isinstance(item, str), f"{field_name}[{i}] must be a string")
        out.append(cast(str, item))  # mypy: item is str after runtime check
    return out


class DataParserAgent(Agent[PipelineState]):
    @property
    def name(self) -> str:
        return "data_parser"

    def run(self, state: PipelineState) -> PipelineState:
        raw: dict[str, Any] = cast(dict[str, Any], state.raw_product)

        require_keys(
            raw,
            [
                "product_name",
                "concentration",
                "skin_type",
                "key_ingredients",
                "benefits",
                "how_to_use",
                "side_effects",
                "price_inr",
            ],
            "RAW_PRODUCT_DATA",
        )

        product_name = str(raw["product_name"])
        concentration = str(raw["concentration"])
        how_to_use = str(raw["how_to_use"])
        side_effects = str(raw["side_effects"])

        skin_type_list = _as_str_list(raw["skin_type"], "skin_type")
        key_ingredients_list = _as_str_list(raw["key_ingredients"], "key_ingredients")
        benefits_list = _as_str_list(raw["benefits"], "benefits")

        price_raw = raw["price_inr"]
        require(isinstance(price_raw, int), "price_inr must be an integer")

        state.product = Product(
            product_name=product_name,
            concentration=concentration,
            skin_type=tuple(skin_type_list),
            key_ingredients=tuple(key_ingredients_list),
            benefits=tuple(benefits_list),
            how_to_use=how_to_use,
            side_effects=side_effects,
            price_inr=price_raw,
        )
        return state
