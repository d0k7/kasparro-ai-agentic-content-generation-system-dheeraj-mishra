# Kasparro Applied AI Engineer Challenge Multi-Agent Content Generation System

This repository implements a **deterministic, modular, agentic content generation system** that converts a single product dataset into **three structured JSON pages** using a **DAG-orchestrated multi-agent pipeline**.

Outputs generated:
- FAQ Page (`faq.json`)
- Product Description Page (`product_page.json`)
- Comparison Page with a **fictional Product B** (`comparison_page.json`)
- DAG metadata (`dag_metadata.json`)

The system emphasizes:
- **Modular agents** with clear responsibilities
- **Reusable logic blocks**
- **Orchestration via DAG**
- **Structured output pipelines**
- Production-quality tooling: **ruff + mypy + pytest (snapshot tests)**

---

## Requirements Met (Assignment Mapping)

- ✅ Parse product input into internal model
- ✅ Generate **≥ 15 categorized questions**
- ✅ Implement your own templates for:
  - FAQ page
  - Product description page
  - Comparison page
- ✅ Logic blocks reused across templates
- ✅ Agents build pages and write structured JSON outputs
- ✅ Comparison includes **fictional Product B**
- ✅ Output JSONs:
  - `outputs/faq.json`
  - `outputs/product_page.json`
  - `outputs/comparison_page.json`
- ✅ Orchestration flow exposed via:
  - `outputs/dag_metadata.json`
- ✅ Clean code + type safety + tests

---

## Project Structure

src/kasparro_agentic/
agents/ # modular agents (parser, question gen, page builders, writer)
core/ # logging, validation, errors
data/ # RAW_PRODUCT_DATA
logic_blocks/ # reusable content logic (faq, product_page, comparison)
templates/ # template engine + page templates + registry
orchestration/ # DAGRunner + Node
pipeline.py # builds DAG and runs pipeline
main.py # CLI entrypoint

tests/
snapshots/ # deterministic expected JSON outputs
test_pipeline.py # snapshot test comparing generated outputs to snapshots
conftest.py # adds src/ to sys.path for tests

docs/
projectdocumentation.md # required documentation (system design + scope + assumptions)



---

## Setup

### Create & activate venv (Windows PowerShell)

python -m venv kaspar
.\kaspar\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt


Quality Checks
ruff check .
mypy src
pytest -q



Run Pipeline (Generate Outputs)

This repo uses a standard src/ layout. Add src to PYTHONPATH before running.

Windows PowerShell

$env:PYTHONPATH="src"
python -m kasparro_agentic --log-level INFO --out-dir outputs

Linux/macOS

PYTHONPATH=src python -m kasparro_agentic --log-level INFO --out-dir outputs


After running, you will have:

outputs/faq.json

outputs/product_page.json

outputs/comparison_page.json

outputs/dag_metadata.json



Orchestration (DAG)

The pipeline is executed using a DAG runner that:

topologically sorts nodes

detects cycles

logs timing for each node

provides describe() for orchestration introspection

The DAG metadata is written to:

outputs/dag_metadata.json

Determinism & No External Data

This implementation is fully deterministic:

No network calls

No randomness

No external facts

All answers and content are derived only from the provided dataset fields

Snapshot tests enforce stable outputs.




