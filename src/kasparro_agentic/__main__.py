from __future__ import annotations

import argparse
from pathlib import Path

from .core.logging import get_logger, setup_logging
from .pipeline import run_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="kasparro_agentic",
        description="Kasparro Agentic Content Generation System (deterministic, modular DAG pipeline)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("outputs"),
        help="Output directory for generated JSON files (default: outputs/)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    setup_logging(args.log_level)
    log = get_logger("kasparro.cli")

    # Prove which module is running (useful on Windows + venvs)
    import kasparro_agentic as pkg  # noqa: WPS433 (local debug import)

    log.info("Running package from: %s", getattr(pkg, "__file__", "<unknown>"))
    log.info("Output dir: %s", args.out_dir.resolve())

    # Run pipeline
    run_pipeline(output_dir=args.out_dir)

    # Confirm outputs
    expected = [
        args.out_dir / "faq.json",
        args.out_dir / "product_page.json",
        args.out_dir / "comparison_page.json",
        args.out_dir / "dag_metadata.json",
    ]
    for p in expected:
        log.info("Wrote: %s | exists=%s", p, p.exists())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
