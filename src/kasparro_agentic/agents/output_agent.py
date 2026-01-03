# src/kasparro_agentic/agents/output_agent.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..core.validation import require


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_outputs(output_dir: Path, state: dict[str, Any]) -> dict[str, Path]:
    require("faq" in state, "missing faq in graph state")
    require("product_page" in state, "missing product_page in graph state")
    require("comparison_page" in state, "missing comparison_page in graph state")
    require("dag_metadata" in state, "missing dag_metadata in graph state")

    faq_path = output_dir / "faq.json"
    product_path = output_dir / "product_page.json"
    comparison_path = output_dir / "comparison_page.json"
    dag_path = output_dir / "dag_metadata.json"

    _write_json(faq_path, state["faq"])
    _write_json(product_path, state["product_page"])
    _write_json(comparison_path, state["comparison_page"])
    _write_json(dag_path, state["dag_metadata"])

    return {
        "faq": faq_path,
        "product_page": product_path,
        "comparison_page": comparison_path,
        "dag_metadata": dag_path,
    }
