# src/kasparro_agentic/data/product_data.py
from __future__ import annotations

from typing import Any

# This is the deterministic seed data used by the pipeline in mock mode/tests.
RAW_PRODUCT_DATA: dict[str, Any] = {
    "product_name": "GlowBoost Vitamin C Serum",
    "brand": "GlowBoost",
    "category": "Skincare",
    "price_inr": 799,
    "key_ingredients": ["10% Vitamin C", "Hyaluronic Acid", "Niacinamide"],
    "benefits": ["Brightening", "Even skin tone", "Antioxidant protection"],
    "skin_type": ["Oily", "Combination"],
    # Keep both fields, because some parts of the codebase may refer to either.
    "concentration": "10% Vitamin C",
    "how_to_use": "Apply 2-3 drops on clean face in the morning. Follow with moisturizer and sunscreen.",
    "side_effects": "No known side effects.",
}
