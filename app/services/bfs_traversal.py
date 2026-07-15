from collections import deque
from app.utils.logger import logger


class BFSTraversal:

    @staticmethod
    def traverse(graph, start_nodes):

        logger.info("Starting BFS traversal")

        queue = deque(start_nodes)

        visited = set()
        order = []

        while queue:
            node = queue.popleft()

            if node in visited:
                continue
            
            visited.add(node)
            order.append(node)

            for child in graph.get(node, []):
                queue.append(child)

        logger.info(
            f"BFS traversal completed: {order}"
        )

        return order