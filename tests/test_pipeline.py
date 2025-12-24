from __future__ import annotations

import json
from pathlib import Path

from kasparro_agentic.pipeline import run_pipeline


def _load_json(path: Path) -> dict:
    """
    Read JSON robustly across OS/editor differences.

    - Windows editors sometimes add UTF-8 BOM to files.
    - `utf-8-sig` transparently strips BOM if present.
    """
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_pipeline_outputs_match_snapshots(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    out_dir = Path("outputs")
    run_pipeline(output_dir=out_dir)

    # Generated outputs
    gen_faq = _load_json(out_dir / "faq.json")
    gen_product = _load_json(out_dir / "product_page.json")
    gen_comp = _load_json(out_dir / "comparison_page.json")

    # Snapshot files shipped with repo
    repo_root = Path(__file__).resolve().parents[1]
    snap_dir = repo_root / "tests" / "snapshots"

    snap_faq = _load_json(snap_dir / "faq.json")
    snap_product = _load_json(snap_dir / "product_page.json")
    snap_comp = _load_json(snap_dir / "comparison_page.json")

    assert gen_faq == snap_faq
    assert gen_product == snap_product
    assert gen_comp == snap_comp

    assert (out_dir / "dag_metadata.json").exists()
