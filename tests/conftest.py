import pytest

from app.models.component import (
    Component,
    HealthCheckRequest
)

@pytest.fixture
def sample_request():
    return HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=[]
            ),
            Component(
                id="B",
                dependencies=["A"]
            ),
            Component(
                id="C",
                dependencies=["B"]
            )
        ]
    )

@pytest.fixture
def sample_components():
    return [
        Component(
            id="A",
            dependencies=[]
        ),
        Component(
            id="B",
            dependencies=["A"]
        ),
        Component(
            id="C",
            dependencies=["B"]
        ),
    ]