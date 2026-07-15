from collections import defaultdict
from app.utils.logger import logger


class DagBuilder:

    @staticmethod
    def build_graph(components):

        logger.info("Building DAG graph")

        graph = defaultdict(list)

        for component in components:
            for dependency in component.dependencies:
                graph[dependency].append(component.id)

        logger.info(
            f"Graph created with {len(components)} components"
        )

        return graph