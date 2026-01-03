from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product:
    product_name: str
    brand: str
    category: str
    price_inr: int

    key_ingredients: tuple[str, ...]
    benefits: tuple[str, ...]
    skin_type: tuple[str, ...]

    # Fields your existing snapshots expect (and your old logic_blocks referenced)
    concentration: str
    how_to_use: str
    side_effects: str


@dataclass(frozen=True, slots=True)
class FictionalProduct:
    product_name: str
    price_inr: int
    key_ingredients: tuple[str, ...]
    benefits: tuple[str, ...]

