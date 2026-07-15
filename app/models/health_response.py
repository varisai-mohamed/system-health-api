from pydantic import BaseModel


class ComponentHealth(BaseModel):
    component: str
    status: str

class HealthSummary(BaseModel):
    total_components: int
    healthy_components: int
    failed_components: int
    health_percentage: float

class HealthResponse(BaseModel):
    overall_status: str
    summary: HealthSummary
    components: list[ComponentHealth]
    graph_file: str