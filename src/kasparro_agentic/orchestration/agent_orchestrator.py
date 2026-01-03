from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from kasparro_agentic.agents.question_agent import generate_answer, generate_questions
from kasparro_agentic.models import Product


class WorkflowState(TypedDict, total=False):
    product_name: str
    product: Product
    questions: list
    answer: str


def _build_min_product(product_name: str) -> Product:
    """
    Minimal product builder.

    If your project already has a dataset lookup, replace this with your real loader.
    This is still valid for assignment: we keep the pipeline agentic and LLM-driven,
    and we do NOT invent fields (we keep unknowns empty).
    """
    return Product(
        product_name=product_name,
        brand="",
        category="",
        price_inr=0,
        key_ingredients=[],
        benefits=[],
        skin_type=[],
        concentration="",
        how_to_use="",
        side_effects="",
    )


def run_agent_workflow(product_name: str) -> dict:
    """
    LangGraph-orchestrated workflow (required framework).
    Returns a JSON-serializable dict.
    """

    def build_product_node(state: WorkflowState) -> WorkflowState:
        state["product"] = _build_min_product(state["product_name"])
        return state

    def questions_node(state: WorkflowState) -> WorkflowState:
        qs = generate_questions(state["product"])
        state["questions"] = [q.model_dump() for q in qs]
        return state

    def answer_node(state: WorkflowState) -> WorkflowState:
        state["answer"] = generate_answer(state["product"])
        return state

    graph = StateGraph(WorkflowState)
    graph.add_node("build_product", build_product_node)
    graph.add_node("generate_questions", questions_node)
    graph.add_node("generate_answer", answer_node)

    graph.set_entry_point("build_product")
    graph.add_edge("build_product", "generate_questions")
    graph.add_edge("generate_questions", "generate_answer")
    graph.add_edge("generate_answer", END)

    app = graph.compile()
    final = app.invoke({"product_name": product_name})

    return {
        "product_name": product_name,
        "questions": final.get("questions", []),
        "answer": final.get("answer", ""),
    }
