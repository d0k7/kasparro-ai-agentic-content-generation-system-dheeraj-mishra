from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..models import PipelineState
from .pages import COMPARISON_TEMPLATE, FAQ_TEMPLATE, PRODUCT_TEMPLATE
from .template_engine import Template


@dataclass(frozen=True, slots=True)
class TemplateRegistry:
    """
    Registry pattern:
    - Adding a new page type becomes a single registry entry + template definition.
    """
    templates: Mapping[str, Template[PipelineState]]

    def get(self, key: str) -> Template[PipelineState]:
        try:
            return self.templates[key]
        except KeyError as e:
            raise KeyError(f"Unknown template key: {key}") from e


DEFAULT_REGISTRY = TemplateRegistry(
    templates={
        "faq": FAQ_TEMPLATE,
        "product_page": PRODUCT_TEMPLATE,
        "comparison_page": COMPARISON_TEMPLATE,
    }
)
