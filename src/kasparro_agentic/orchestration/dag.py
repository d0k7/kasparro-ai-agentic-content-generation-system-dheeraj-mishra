from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from kasparro_agentic.agents.question_agent import generate_answer, generate_questions
from kasparro_agentic.llm.provider import build_llm_provider
from kasparro_agentic.models import Product, Question


class GraphState(TypedDict, total=False):
    product_name: str
    product: Product
    questions: list[Question]
    answer: str
    error: str | None
    mode: str


def _node_build_product(state: GraphState) -> GraphState:
    product_name = state["product_name"].strip()
    product = Product(product_name=product_name)
    return {"product": product}


def _node_generate_questions(state: GraphState) -> GraphState:
    product = state["product"]
    qs = generate_questions(product)
    return {"questions": qs}


def _node_generate_answer(state: GraphState) -> GraphState:
    product = state["product"]
    # standard question for demo
    q = f"What is {product.product_name} and how do I use it safely?"
    ans = generate_answer(product, q)
    return {"answer": ans}


def _node_metadata(state: GraphState) -> GraphState:
    # record mode for debugging
    mode = (build_llm_provider().__class__.__name__).lower()
    return {"mode": mode}


def _build_graph():
    g = StateGraph(GraphState)

    g.add_node("build_product", _node_build_product)
    g.add_node("questions", _node_generate_questions)
    g.add_node("answer", _node_generate_answer)
    g.add_node("metadata", _node_metadata)

    g.set_entry_point("build_product")
    g.add_edge("build_product", "questions")
    g.add_edge("questions", "answer")
    g.add_edge("answer", "metadata")
    g.add_edge("metadata", END)

    return g.compile()


_GRAPH = _build_graph()


def run_workflow(product_name: str) -> dict:
    """
    Backend LangGraph workflow (safe default is mock provider).
    Returns a JSON-serializable dict.
    """
    init: GraphState = {"product_name": product_name}
    try:
        out = _GRAPH.invoke(init)
        product: Product = out.get("product")  # type: ignore[assignment]
        questions: list[Question] = out.get("questions", [])  # type: ignore[assignment]
        answer: str = out.get("answer", "")

        return {
            "productName": product.product_name if product else product_name,
            "questions": [q.question for q in questions],
            "answer": answer,
            "mode": out.get("mode", "mock"),
            "error": None,
        }
    except Exception as e:  # noqa: BLE001
        return {
            "productName": product_name,
            "questions": [],
            "answer": "",
            "mode": "error",
            "error": str(e),
        }


# Backward-compatible name (some earlier code calls this)
def run_agent_workflow(product_name: str) -> dict:
    return run_workflow(product_name)
