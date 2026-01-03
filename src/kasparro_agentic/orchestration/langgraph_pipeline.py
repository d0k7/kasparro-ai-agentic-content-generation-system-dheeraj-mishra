from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any, TypedDict

from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, StateGraph

from kasparro_agentic.agents.page_agents import (
    build_comparison_page_agent,
    build_faq_page_agent,
    build_fictional_product_b_agent,
    build_product_page_agent,
)
from kasparro_agentic.agents.parser_agent import parse_product
from kasparro_agentic.agents.question_agent import generate_questions
from kasparro_agentic.data.product_data import RAW_PRODUCT_DATA


class GraphState(TypedDict, total=False):
    product: Any
    questions: Any
    faq: Any
    product_page: Any
    fictional_product_b: Any
    comparison_page: Any
    dag_metadata: Any


def timed(name: str) -> Callable[[Callable[[GraphState], dict[str, Any]]], Callable[[GraphState], dict[str, Any]]]:
    def decorator(fn: Callable[[GraphState], dict[str, Any]]) -> Callable[[GraphState], dict[str, Any]]:
        def wrapper(state: GraphState) -> dict[str, Any]:
            _start = time.time()
            out = fn(state)
            _ = int((time.time() - _start) * 1000)
            return out
        return wrapper
    return decorator


def build_graph() -> Any:
    g: Any = StateGraph(GraphState)

    @timed("data_parser")
    def node_data_parser(_: GraphState) -> dict[str, Any]:
        product = parse_product(RAW_PRODUCT_DATA)
        return {"product": product}  # ✅ partial write only

    @timed("question_generator")
    def node_question_generator(state: GraphState) -> dict[str, Any]:
        questions = generate_questions(state["product"])
        return {"questions": questions}  # ✅ partial write only

    @timed("faq_page_builder")
    def node_faq_builder(state: GraphState) -> dict[str, Any]:
        faq = build_faq_page_agent(state["product"], state["questions"])
        return {"faq": faq}  # ✅ partial write only

    @timed("product_page_builder")
    def node_product_builder(state: GraphState) -> dict[str, Any]:
        page = build_product_page_agent(state["product"])
        return {"product_page": page}  # ✅ partial write only

    @timed("comparison_page_builder")
    def node_comparison_builder(state: GraphState) -> dict[str, Any]:
        product_a = state["product"]
        product_b = build_fictional_product_b_agent(product_a)
        comp = build_comparison_page_agent(product_a, product_b)
        return {"fictional_product_b": product_b, "comparison_page": comp}  # ✅ partial write only

    @timed("dag_metadata_writer")
    def node_metadata(_: GraphState) -> dict[str, Any]:
        return {
            "dag_metadata": {
                "framework": "langgraph",
                "execution_order": [
                    "data_parser",
                    "question_generator",
                    "faq_page_builder",
                    "product_page_builder",
                    "comparison_page_builder",
                    "dag_metadata_writer",
                    "output_writer",
                ],
                "nodes": [
                    {"name": "data_parser", "depends_on": []},
                    {"name": "question_generator", "depends_on": ["data_parser"]},
                    {"name": "faq_page_builder", "depends_on": ["question_generator"]},
                    {"name": "product_page_builder", "depends_on": ["data_parser"]},
                    {"name": "comparison_page_builder", "depends_on": ["data_parser"]},
                    {
                        "name": "dag_metadata_writer",
                        "depends_on": ["faq_page_builder", "product_page_builder", "comparison_page_builder"],
                    },
                    {"name": "output_writer", "depends_on": ["dag_metadata_writer"]},
                ],
            }
        }

    g.add_node("data_parser", RunnableLambda(node_data_parser))
    g.add_node("question_generator", RunnableLambda(node_question_generator))
    g.add_node("faq_page_builder", RunnableLambda(node_faq_builder))
    g.add_node("product_page_builder", RunnableLambda(node_product_builder))
    g.add_node("comparison_page_builder", RunnableLambda(node_comparison_builder))
    g.add_node("dag_metadata_writer", RunnableLambda(node_metadata))

    g.set_entry_point("data_parser")
    g.add_edge("data_parser", "question_generator")
    g.add_edge("question_generator", "faq_page_builder")

    g.add_edge("data_parser", "product_page_builder")
    g.add_edge("data_parser", "comparison_page_builder")

    g.add_edge("faq_page_builder", "dag_metadata_writer")
    g.add_edge("product_page_builder", "dag_metadata_writer")
    g.add_edge("comparison_page_builder", "dag_metadata_writer")

    g.add_edge("dag_metadata_writer", END)
    return g.compile()
