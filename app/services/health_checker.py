import asyncio
import random

from app.utils.logger import logger
from app.models.health_response import ComponentHealth


class HealthChecker:

    @staticmethod
    async def check_component(component_id):

        logger.info(
            f"Checking health of component {component_id}"
        )

        await asyncio.sleep(1)

        status = random.choice(
            ["HEALTHY", "HEALTHY", "FAILED"]
        )

        logger.info(
            f"Component {component_id} status: {status}"
        )

        if status == "FAILED":
            logger.warning(
                f"Component {component_id} reported FAILED status"
            )

        return ComponentHealth(
            component= component_id,
            status= status
        )
    