# Problem Statement

Build a modular agentic system that transforms a small product dataset into structured JSON pages:
FAQ, Product Description, and Comparison, using reusable logic blocks and an orchestration flow.

# Solution Overview

We implement a **modular**, **agentic**, **LLM-powered** pipeline:
- Parse input -> internal model
- Generate categorized user questions (>=15) via real LLM (using **Puter**)
- Build pages through templates + reusable content logic blocks
- Validate page payloads
- Emit machine-readable JSON outputs

All work is performed by agents connected through a **DAG orchestrator**.

### **Key Components:**
1. **LangChain**: Used for managing large language models (LLMs) to generate questions and answers dynamically.
2. **LangGraph**: Orchestrates the workflow through a **Directed Acyclic Graph (DAG)**, defining clear dependencies between tasks.
3. **Puter Integration**: Real LLM integration through Puter, enabling dynamic, real-time content generation based on the product dataset.

# Scope & Assumptions
- **Real-time LLM Integration**: Uses **Puter** and **LangChain** for dynamic question and answer generation.
- **LangGraph Workflow**: Orchestrates the entire content generation process using a dependency graph, ensuring clear task order.
- Product B in the comparison is explicitly fictional and generated internally.
- **Content is not rule-based** but powered by real LLMs for more intelligent, dynamic responses.

# System Design

This assignment expects two core engineering signals:
1) **Agentization**: Split the pipeline into modular, single-responsibility units.
2) **Orchestration**: Run those units via an explicit dependency graph (DAG), not a hard-coded sequence.

<<<<<<< HEAD
# System Design
This assignment expects two core engineering signals:
1) **Agentization**: split the pipeline into modular, single-responsibility units.
2) **Orchestration**: run those units via an explicit dependency graph (DAG), not a hard-coded sequence.


=======
>>>>>>> c4112bd (Updated README, project documentation, and LLM integration)
## Agents (Single Responsibility)
- **DataParserAgent**: Raw data -> Product model
- **QuestionGenerationAgent**: Product -> Categorized questions (>=15) using **Puter** and **LangChain**.
- **FAQPageAgent**: Template rendering and validation -> FAQ page dict.
- **ProductPageAgent**: Template rendering and validation -> Product page dict.
- **ComparisonPageAgent**: Template rendering and validation -> Comparison page dict.
- **DagMetadataAgent**: Writes orchestration metadata (`dag_metadata.json`).
- **OutputWriterAgent**: Writes final JSON outputs.

## Orchestration Graph
- **DAGRunner**: Executes nodes topologically, ensuring proper task order.
- **DAGRunner Introspection**: Provides `describe()` for introspection.
- `dag_metadata.json` demonstrates orchestration transparency.

## Reusable Logic Blocks
- Logic blocks are pure functions located in `logic_blocks/`:
  - **faq.py**: Deterministic Q/A rules and FAQ assembly.
  - **product_page.py**: Summary and highlights builders.
  - **comparison.py**: Fictional product builder and comparison builder.

## Template Engine + Registry
- **Templates** are structural field resolvers (not string templates) to guarantee strict JSON.
- **Template Registry**: Adding a new page type is a clean extension:
  - Define a template.
  - Register the key.
  - Add the corresponding agent.

# Frontend (User Interaction)

- The system also includes a **local frontend** running on **localhost**, where users can enter product names and interact with the system for content generation.
  - The **frontend** allows users to input a product name.
  - The backend (powered by **Puter** and **LangChain**) dynamically generates:
    - Product-related **questions**
    - **Answers** to the questions
  - The content is generated using **LLMs**, ensuring that the questions and answers are tailored to the specific product.

# Quality Gates
- **Validation**: Strict checks on required keys and minimal types.
- **Snapshot tests**: Ensures output JSON stability across refactors.
- **CI**: **Ruff**, **Mypy**, and **Pytest** run on every push/PR.


<<<<<<< HEAD
# Diagram (Conceptual)
raw_product -> parser -> question_gen -> { faq_builder, product_builder, comparison_builder } -> metadata -> writer
=======
>>>>>>> c4112bd (Updated README, project documentation, and LLM integration)
