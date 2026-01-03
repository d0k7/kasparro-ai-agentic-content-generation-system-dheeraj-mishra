# src/kasparro_agentic/data/product_store.py

from __future__ import annotations

import csv
import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from kasparro_agentic.models import Product


def _as_list(x: Any) -> list[str]:
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i).strip() for i in x if str(i).strip()]
    # allow comma-separated strings
    s = str(x).strip()
    if not s:
        return []
    return [p.strip() for p in s.split(",") if p.strip()]


def _coerce_int(x: Any, default: int = 0) -> int:
    try:
        if x is None:
            return default
        if isinstance(x, (int, float)):
            return int(x)
        s = str(x).strip()
        if not s:
            return default
        # remove currency symbols etc
        s = "".join(ch for ch in s if ch.isdigit())
        return int(s) if s else default
    except Exception:
        return default


def _coerce_str(x: Any, default: str = "") -> str:
    if x is None:
        return default
    s = str(x).strip()
    return s if s else default


def _product_from_dict(d: dict[str, Any]) -> Product:
    return Product(
        product_name=_coerce_str(d.get("product_name") or d.get("name") or d.get("title")),
        brand=_coerce_str(d.get("brand")),
        category=_coerce_str(d.get("category")),
        price_inr=_coerce_int(d.get("price_inr") or d.get("price") or d.get("mrp")),
        key_ingredients=_as_list(d.get("key_ingredients") or d.get("ingredients")),
        benefits=_as_list(d.get("benefits")),
        skin_type=_as_list(d.get("skin_type") or d.get("skin_types")),
        concentration=_coerce_str(d.get("concentration")),
        how_to_use=_coerce_str(d.get("how_to_use") or d.get("usage")),
        side_effects=_coerce_str(d.get("side_effects") or d.get("warnings")),
    )


def _iter_json_products(path: Path) -> Iterable[Product]:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Updated to use the 'X | Y' style for isinstance
    items = data.get("products", []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    for item in items:
        if isinstance(item, dict):
            p = _product_from_dict(item)
            if p.product_name:
                yield p


def _iter_csv_products(path: Path) -> Iterable[Product]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = _product_from_dict(dict(row))
            if p.product_name:
                yield p


def load_product_by_name(product_name: str) -> Product:
    """
    Looks up the product from a dataset file if available.

    Supported:
      - JSON: data/products.json OR path via KASPARRO_DATA_PATH
      - CSV : data/products.csv  OR path via KASPARRO_DATA_PATH

    If no dataset is found or no match: returns a minimal Product with only product_name.
    """
    target = product_name.strip()
    if not target:
        return Product(
            product_name="",
            brand="",
            category="",
            price_inr=0,
            key_ingredients=[],
            benefits=[],
            skin_type=[],
            concentration="",
            how_to_use="",
            side_effects="",
        )

    # choose dataset path
    env_path = os.getenv("KASPARRO_DATA_PATH", "").strip()
    candidates: list[Path] = []
    if env_path:
        candidates.append(Path(env_path))

    # common defaults
    root = Path(__file__).resolve().parents[2]  # .../src
    candidates += [
        root / "data" / "products.json",
        root / "data" / "products.csv",
        root.parent / "data" / "products.json",
        root.parent / "data" / "products.csv",
    ]

    products: list[Product] = []
    for c in candidates:
        if not c.exists() or not c.is_file():
            continue
        if c.suffix.lower() == ".json":
            products.extend(list(_iter_json_products(c)))
        elif c.suffix.lower() == ".csv":
            products.extend(list(_iter_csv_products(c)))

    # match by case-insensitive exact name first, then contains
    t = target.lower()
    exact = [p for p in products if p.product_name.lower() == t]
    if exact:
        return exact[0]
    contains = [p for p in products if t in p.product_name.lower()]
    if contains:
        return contains[0]

    # fallback minimal
    return Product(
        product_name=target,
        brand="",
        category="",
        price_inr=0,
        key_ingredients=[],
        benefits=[],
        skin_type=[],
        concentration="",
        how_to_use="",
        side_effects="",
    )
