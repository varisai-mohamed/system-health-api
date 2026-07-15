from pydantic import BaseModel, Field
from typing import List


class Component(BaseModel):
    id: str = Field(
        min_length=1,
        description="Component ID"
    )

    dependencies: List[str] = []

class HealthCheckRequest(BaseModel):
    components: List[Component]