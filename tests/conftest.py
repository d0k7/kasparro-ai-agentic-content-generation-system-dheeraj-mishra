from __future__ import annotations

import sys
from pathlib import Path

# Ensure "src/" is on sys.path so `import kasparro_agentic` works in tests.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))
