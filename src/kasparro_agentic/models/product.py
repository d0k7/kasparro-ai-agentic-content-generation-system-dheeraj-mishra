from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product:
    """Normalized internal representation of the (only) input product dataset."""
    product_name: str
    concentration: str
    skin_type: tuple[str, ...]
    key_ingredients: tuple[str, ...]
    benefits: tuple[str, ...]
    how_to_use: str
    side_effects: str
    price_inr: int


@dataclass(frozen=True, slots=True)
class FictionalProduct:
    """A fictional comparison product (allowed by the assignment)."""
    product_name: str
    key_ingredients: tuple[str, ...]
    benefits: tuple[str, ...]
    price_inr: int

    @staticmethod
    def build_default() -> FictionalProduct:
        # Keep it clearly fictional but structured.
        return FictionalProduct(
            product_name="RadiantFix Niacinamide Serum (Fictional)",
            key_ingredients=("Niacinamide", "Panthenol"),
            benefits=("Oil control", "Helps even-looking tone"),
            price_inr=799,
        )
