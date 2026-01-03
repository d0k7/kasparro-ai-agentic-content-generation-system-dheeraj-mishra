from __future__ import annotations

# Export only what actually exists.
from .comparison import build_fictional_product_b
from .comparison_page import build_comparison_page
from .faq import build_faq_page
from .product_page import build_product_page

__all__ = [
    "build_faq_page",
    "build_product_page",
    "build_fictional_product_b",
    "build_comparison_page",
]
