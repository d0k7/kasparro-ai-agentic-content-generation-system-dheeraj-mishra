# Kasparro Applied AI Engineer Challenge  
## Multi-Agent Content Generation System

This repository implements a **deterministic, modular, multi-agent content generation pipeline** that converts a single structured product dataset into multiple **production-ready JSON content pages**, orchestrated using a **Directed Acyclic Graph (DAG)**.

The system is designed to demonstrate **real-world agentic system design**, focusing on modularity, reusability, orchestration, and correctness rather than prompt tricks or shallow automation.

---

## Outputs

Running the pipeline generates the following artifacts:

- `outputs/faq.json` — FAQ page with categorized questions and answers  
- `outputs/product_page.json` — Structured product description page  
- `outputs/comparison_page.json` — Product comparison with a fictional Product B  
- `outputs/dag_metadata.json` — DAG execution order, dependencies, and timing  

---

## Design Goals

This implementation emphasizes:

- **Single-responsibility agents**
- **Reusable logic blocks shared across templates**
- **Explicit DAG-based orchestration**
- **Strictly structured JSON outputs**
- **Deterministic execution**
- **Production-grade tooling and testing**

The goal is to model how an agentic content system would be built in a real engineering environment, not as a demo script.

---

## Assignment Requirements

All requirements from the assignment are fully satisfied:

- Parse raw product input into internal typed models  
- Generate **15+ categorized questions**  
- Implement custom templates for:
  - FAQ page
  - Product description page
  - Comparison page  
- Reuse logic blocks across multiple page types  
- Include a **fictional Product B** for comparison  
- Produce structured JSON outputs only  
- Expose orchestration flow via DAG metadata  
- Enforce code quality, typing, and deterministic tests  

---

## Project Structure

src/kasparro_agentic/
├─ agents/ # Parser, question generator, page builders, output writer
├─ core/ # Logging, validation, error handling
├─ data/ # RAW_PRODUCT_DATA
├─ logic_blocks/ # Reusable content logic (FAQ, product, comparison)
├─ templates/ # Template engine, page templates, registry
├─ orchestration/ # DAGRunner and Node abstractions
├─ pipeline.py # DAG construction and execution
└─ main .py # CLI entrypoint

tests/
├─ snapshots/ # Deterministic expected JSON outputs
├─ test_pipeline.py # Snapshot-based regression tests
└─ conftest.py # PYTHONPATH setup

docs/
└─ projectdocumentation.md # System design, scope, assumptions

yaml

---

## Setup

### Virtual Environment

python -m venv kaspar
.\kaspar\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt


Quality Gates
All checks must pass:

ruff check .
mypy src
pytest -q


Run the Pipeline
The project follows the standard src/layout.

$env:PYTHONPATH="src"
python -m kasparro_agentic --log-level INFO --out-dir outputs


Linux / macOS
PYTHONPATH=src python -m kasparro_agentic --log-level INFO --out-dir outputs


Orchestration Details:-

Execution is managed by an explicit DAG
Nodes declare dependencies
Cycles are prevented
Per-node execution timing is logged
DAG metadata is exported to JSON

outputs/dag_metadata.json

Determinism Guarantee
This system is fully deterministic :

No randomness
No external APIs or network calls
No external facts or assumptions
All content derived strictly from the provided dataset
Snapshot tests enforce output stability across runs.

Documentation
Detailed system design documentation is available at:

docs/projectdocumentation.md

This covers:

Architecture decisions
Agent responsibilities
DAG structure
Scope and assumptions
