from __future__ import annotations

import json
from pathlib import Path

from ..core.validation import require
from ..models import PipelineState
from .base import Agent


class DagMetadataAgent(Agent[PipelineState]):
    """
    Writes orchestration metadata to disk for transparency.
    Not required by the assignment, but demonstrates real engineering discipline.
    """

    @property
    def name(self) -> str:
        return "dag_metadata_writer"

    def run(self, state: PipelineState) -> PipelineState:
        require(state.dag_metadata is not None, "DagMetadataAgent: dag_metadata missing.")

        out_dir = state.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)

        path = Path(out_dir) / "dag_metadata.json"
        path.write_text(
            json.dumps(state.dag_metadata, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return state
