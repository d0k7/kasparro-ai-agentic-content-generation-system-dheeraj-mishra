from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core.validation import require
from ..models import PipelineState
from .base import Agent


class OutputWriterAgent(Agent[PipelineState]):
    @property
    def name(self) -> str:
        return "output_writer"

    def run(self, state: PipelineState) -> PipelineState:
        out_dir = state.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        self._write(out_dir / "faq.json", state.faq_page, "faq_page")
        self._write(out_dir / "product_page.json", state.product_page, "product_page")
        self._write(out_dir / "comparison_page.json", state.comparison_page, "comparison_page")

        return state

    def _write(self, path: Path, obj: Any, field_name: str) -> None:
        require(obj is not None, f"OutputWriterAgent: missing required page: {field_name}")

        path.write_text(
            json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
