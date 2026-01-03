# src/kasparro_agentic/pipeline.py
from __future__ import annotations

from pathlib import Path

from .agents.output_agent import write_outputs
from .orchestration.langgraph_pipeline import build_graph


def run_pipeline(output_dir: Path) -> dict[str, Path]:
    graph = build_graph()
    state = graph.invoke({})  # returns dict-like GraphState
    return write_outputs(output_dir, state)
