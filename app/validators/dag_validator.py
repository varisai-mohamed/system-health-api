from app.exceptions.api_exception import ApiException
from app.utils.logger import logger


class DagValidator:

    @staticmethod
    def validate(request):

        logger.info("Starting DAG validation")

        DagValidator.validate_components_exist(request)

        DagValidator.validate_unique_ids(request)

        DagValidator.validate_dependencies_exist(request)

        DagValidator.validate_self_dependency(request)

        DagValidator.validate_cycle(request)

    @staticmethod
    def validate_components_exist(request):

        logger.info("Validating components list")

        if not request.components:
            logger.error("No components provided")

            raise ApiException(
                status_code=400,
                message="At least one component is required."
            )
        
    @staticmethod
    def validate_unique_ids(request):

        logger.info("Validating unique component IDs")

        ids = [
            component.id 
            for component in request.components
        ]
        
        duplicate_ids = {
            component_id
            for component_id in ids
            if ids.count(component_id) > 1
        }

        if duplicate_ids:

            logger.error(
                f"Duplicate component IDs detected: {duplicate_ids}"
            )

            raise ApiException(
                status_code=400,
                message=f"Duplicate component IDs detected: {list(duplicate_ids)}"
            )
        
    @staticmethod
    def validate_dependencies_exist(request):

        logger.info("Validating dependencies")

        component_ids = {
            component.id
            for component in request.components
        }

        for component in request.components:

            for dependency in component.dependencies:

                if dependency not in component_ids:

                    logger.error(
                        f"Dependency '{dependency}' not found for component '{component.id}'"
                    )

                    raise ApiException(
                        status_code=400,
                        message=f"Dependency '{dependency}' not found." 
                    )
                
    @staticmethod
    def validate_self_dependency(request):

        logger.info("Validating self dependencies")

        for component in request.components:

            if component.id in component.dependencies:

                logger.error(
                    f"Self dependency detected for component '{component.id}'"
                )

                raise ApiException(
                    status_code=400,
                    message=f"Self dependency detected for '{component.id}'."
                )
            
    @staticmethod
    def validate_cycle(request):

        logger.info("Validating circular dependencies")

        graph = {}

        for component in request.components:
            graph[component.id] = component.dependencies

        visited = set()
        recursion_stack = set()

        def dfs(node):

            visited.add(node)
            recursion_stack.add(node)

            for neighbour in graph.get(node, []):

                if neighbour not in visited:

                    if dfs(neighbour):
                        return True
                    
                elif neighbour in recursion_stack:
                    return True
                
            recursion_stack.remove(node)

            return False
        
        for node in graph:

            if node not in visited:

                if dfs(node):

                    logger.error(
                        f"Circular dependency detected involving node '{node}'"
                    )

                    raise ApiException(
                        status_code=400,
                        message="Circular dependency detected. Graph must be a DAG."
                    )
                