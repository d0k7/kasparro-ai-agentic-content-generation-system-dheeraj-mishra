# Problem Statement
Build a modular agentic system that transforms a small product dataset into structured JSON pages:
FAQ, Product Description, and Comparison, using reusable logic blocks and an orchestration flow.

# Solution Overview
We implement a deterministic multi-agent pipeline:
- Parse input -> internal model
- Generate categorized user questions (>=15)
- Build pages through templates + reusable content logic blocks
- Validate page payloads
- Emit machine-readable JSON outputs

All work is performed by agents connected through a DAG orchestrator.

# Scope & Assumptions
- No external facts or research are used beyond the provided dataset.
- Product B in the comparison is explicitly fictional and generated internally.
- Content is deterministic and rule-based for repeatability and testability.

# System Design (Most Important)
## Agents (Single Responsibility)
- DataParserAgent: raw dict -> Product model
- QuestionGenerationAgent: Product -> categorized questions (>=15)
- FAQPageAgent: Template render + validations -> faq_page dict
- ProductPageAgent: Template render + validations -> product_page dict
- ComparisonPageAgent: Template render + validations -> comparison_page dict
- DagMetadataAgent: writes orchestration metadata (dag_metadata.json)
- OutputWriterAgent: writes final JSON outputs

## Orchestration Graph
- DAGRunner executes nodes topologically.
- DAGRunner provides `describe()` for introspection.
- dag_metadata.json demonstrates orchestration transparency.

## Reusable Logic Blocks
Logic blocks are pure functions in `logic_blocks/`:
- faq.py: deterministic Q/A rules + FAQ assembly
- product_page.py: summary/highlights builders
- comparison.py: fictional product builder + comparison builder

## Template Engine + Registry
- Templates are structural field resolvers (not string templates) to guarantee strict JSON.
- Template Registry makes adding a new page type a clean extension:
  - Define template
  - Register key
  - Add agent 

## Quality Gates
- Validation: strict checks on required keys and minimal types
- Snapshot tests: output JSON stability across refactors
- CI: ruff + mypy + pytest run on every push/PR

# Diagram (Conceptual)
raw_product -> parser -> question_gen -> { faq_builder, product_builder, comparison_builder } -> metadata -> writer
