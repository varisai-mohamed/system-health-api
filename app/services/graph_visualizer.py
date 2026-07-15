from graphviz import Digraph
from datetime import datetime
from pathlib import Path

from app.utils.logger import logger


class GraphVisualizer:

    @staticmethod
    def generate_graph(
        components,
        health_results
    ):
        
        logger.info(
            "Generating DAG graph image"
        )

        dot = Digraph(
            comment="System Health DAG"
        )
        
        status_map = {
            result.component: result.status
            for result in health_results
        }

        for component in components:

            color = (
                "red"
                if status_map.get(component.id) == "FAILED"
                else "lightgreen"
            )

            dot.node(
                component.id,
                component.id,
                style="filled",
                fillcolor=color
            )

        for component in components:

            for dependency in component.dependencies:

                dot.edge(
                    dependency,
                    component.id
                )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("generated_graphs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"dag_{timestamp}"

        dot.render(
            output_file,
            format="png",
            cleanup=True
        )

        logger.info(
            "DAG graph generated succesfully"
        )
    
        return str(output_file.with_suffix(".png"))