from __future__ import annotations

from typing import Any

from kasparro_agentic.models import Product


def _as_tuple_str(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()

    # ✅ ruff UP038: use X | Y instead of (X, Y)
    if isinstance(value, list | tuple):
        return tuple(str(x).strip() for x in value if str(x).strip())

    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",")]
        return tuple(p for p in parts if p)

    s = str(value).strip()
    return (s,) if s else tuple()


def _as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_str(value: Any, default: str) -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s else default


def parse_product(raw: dict[str, Any]) -> Product:
    return Product(
        product_name=_as_str(raw.get("product_name"), "Unknown Product"),
        brand=_as_str(raw.get("brand"), "Unknown"),
        category=_as_str(raw.get("category"), "Unknown"),
        price_inr=_as_int(raw.get("price_inr"), 0),
        key_ingredients=_as_tuple_str(raw.get("key_ingredients")),
        benefits=_as_tuple_str(raw.get("benefits")),
        skin_type=_as_tuple_str(raw.get("skin_type")),
        concentration=_as_str(raw.get("concentration"), "Not specified in the provided dataset."),
        how_to_use=_as_str(raw.get("how_to_use"), "Not specified in the provided dataset."),
        side_effects=_as_str(raw.get("side_effects"), "Not specified in the provided dataset."),
    )
