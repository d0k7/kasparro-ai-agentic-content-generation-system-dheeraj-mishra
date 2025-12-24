from __future__ import annotations

from pathlib import Path

from .agents import (
    ComparisonPageAgent,
    DagMetadataAgent,
    DataParserAgent,
    FAQPageAgent,
    OutputWriterAgent,
    ProductPageAgent,
    QuestionGenerationAgent,
)
from .data.product_input import RAW_PRODUCT_DATA
from .models import PipelineState
from .orchestration import DAGRunner, Node


def run_pipeline(output_dir: Path) -> PipelineState:
    state = PipelineState(raw_product=RAW_PRODUCT_DATA, output_dir=output_dir)

    parser = DataParserAgent()
    qgen = QuestionGenerationAgent()
    faq = FAQPageAgent()
    product_page = ProductPageAgent()
    comparison = ComparisonPageAgent()
    dag_meta = DagMetadataAgent()
    writer = OutputWriterAgent()

    nodes: list[Node[PipelineState]] = [
        Node(name=parser.name, depends_on=tuple(), run=parser.run),
        Node(name=qgen.name, depends_on=(parser.name,), run=qgen.run),
        Node(name=faq.name, depends_on=(qgen.name,), run=faq.run),
        Node(name=product_page.name, depends_on=(parser.name,), run=product_page.run),
        Node(name=comparison.name, depends_on=(parser.name,), run=comparison.run),
        Node(name=dag_meta.name, depends_on=(faq.name, product_page.name, comparison.name), run=dag_meta.run),
        Node(name=writer.name, depends_on=(dag_meta.name,), run=writer.run),
    ]

    dag: DAGRunner[PipelineState] = DAGRunner(nodes=nodes)

    # attach DAG metadata before run (explicit; not hidden global state)
    state.dag_metadata = dag.describe()

    return dag.run(state)
