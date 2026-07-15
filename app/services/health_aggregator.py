from app.utils.logger import logger
from app.models.health_response import (
    ComponentHealth,
    HealthSummary
)

class HealthAggregator:
  
    @staticmethod
    def propagate_failures(
        components,
        health_results
    ):
        
        logger.info(
            "Starting dependency failure propagation"
        )

        status_map={
            result.component: result.status
            for result in health_results
        }

        dependency_map = {
            component.id: component.dependencies
            for component in components
        }

        changed = True

        while changed:

            changed = False

            for component_id, dependencies in dependency_map.items():

                for dependency in dependencies:

                    if status_map.get(dependency) == "FAILED" :

                        if status_map.get(component_id) != "FAILED":

                            logger.warning(
                                f"Component '{component_id}' marked FAILED because dependency '{dependency}' failed"
                            )

                            status_map[component_id] = "FAILED"

                            changed = True


        return[
            ComponentHealth(
                component= component_id,
                status= status
            )
            for component_id, status in status_map.items()
        ]
        
    
    @staticmethod
    def calculate_system_health(results):

        for result in results:

            if result.status == "FAILED":
                return "UNHEALTHY"

        return "HEALTHY"

    @staticmethod
    def build_summary(results):

        total = len(results)

        healthy = sum(
            1
            for result in results
            if result.status == "HEALTHY"
        )

        failed = sum(
            1
            for result in results
            if result.status == "FAILED"
        )

        health_percentage = round(
            (healthy / total) * 100, 2
        )

        return HealthSummary(
            total_components= total,
            healthy_components= healthy,
            failed_components= failed,
            health_percentage= health_percentage
        )
    
    