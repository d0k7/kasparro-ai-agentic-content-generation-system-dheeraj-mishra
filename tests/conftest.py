# tests/conftest.py
from __future__ import annotations

import os
import sys
from pathlib import Path


def pytest_configure() -> None:
    # Ensure src/ layout works in tests
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"
    sys.path.insert(0, str(src_path))

    # Deterministic tests: always use mock provider
    os.environ["KASPARRO_LLM_MODE"] = "mock"
