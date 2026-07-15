from app.services.health_aggregator import HealthAggregator
from app.models.component import Component

from app.models.health_response import (
    ComponentHealth
)

def test_propagate_failures_all_healthy():

    components = [
        Component(id="A", dependencies=[]),
        Component(id="B", dependencies=["A"])
    ]

    results = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="B",
            status="HEALTHY"
        )
    ]

    updated_results = (
        HealthAggregator.propagate_failures(
            components, 
            results
        )
    )

    status_map = {
        result.component: result.status
        for result in updated_results
    }

    assert status_map["A"] == "HEALTHY"
    assert status_map["B"] == "HEALTHY"


def test_propagate_failures_dependency_failed():

    components = [
        Component(id="A", dependencies=[]),
        Component(id="B", dependencies=["A"])
    ]

    results = [
        ComponentHealth(
            component="A",
            status="FAILED"
        ),
        ComponentHealth(
            component="B",
            status="HEALTHY"
        )
    ]

    updated_results = (
        HealthAggregator.propagate_failures(
            components, 
            results
        )
    )

    status_map = {
        result.component: result.status
        for result in updated_results
    }

    assert status_map["A"] == "FAILED"
    assert status_map["B"] == "FAILED"


def test_propagate_failures_multiple_levles():

    components = [
        Component(id="A", dependencies=[]),
        Component(id="B", dependencies=["A"]),
        Component(id="C", dependencies=["B"])
    ]

    results = [
        ComponentHealth(
            component="A",
            status="FAILED"
        ),
        ComponentHealth(
            component="B",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="C",
            status="HEALTHY"
        )
    ]

    updated_results = (
        HealthAggregator.propagate_failures(
            components, 
            results
        )
    )

    status_map = {
        result.component: result.status
        for result in updated_results
    }

    assert status_map["A"] == "FAILED"
    assert status_map["B"] == "FAILED"
    assert status_map["C"] == "FAILED"


def test_calculate_system_health_healthy():

    results = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="B",
            status="HEALTHY"
        )
    ]

    status = (
        HealthAggregator.calculate_system_health(
            results
        )
    )

    assert status == "HEALTHY"


def test_calculate_system_health_unhealthy():

    results = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="B",
            status="FAILED"
        )
    ]

    status = (
        HealthAggregator.calculate_system_health(
            results
        )
    )

    assert status == "UNHEALTHY"


def test_build_summary():

    results = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="B",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="C",
            status="FAILED"
        )
    ]

    summary = (
        HealthAggregator.build_summary(
            results
        )
    )

    assert summary.total_components == 3
    assert summary.healthy_components == 2
    assert summary.failed_components == 1
    assert summary.health_percentage == 66.67


