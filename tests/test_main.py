from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.health_response import (
    ComponentHealth,
    HealthSummary
)


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "System Health Check API"
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


@patch("app.main.GraphVisualizer.generate_graph")
@patch("app.main.HealthAggregator.build_summary")
@patch("app.main.HealthAggregator.calculate_system_health")
@patch("app.main.HealthAggregator.propagate_failures")
@patch("app.main.HealthChecker.check_component")
@patch("app.main.BFSTraversal.traverse")
@patch("app.main.DagBuilder.build_graph")
@patch("app.main.DagValidator.validate")
def test_check_health_success(
    mock_validate,
    mock_build_graph,
    mock_traverse,
    mock_check_component,
    mock_propagate_failures,
    mock_calculate_system_health,
    mock_build_summary,
    mock_generate_graph
):
    mock_build_graph.return_value = {
        "A": ["B"]
    }

    mock_traverse.return_value = [
        "A", 
        "B"
    ]

    async def mock_health_check(component_id):
        return ComponentHealth(
            component=component_id,
            status="HEALTHY"
        )

    mock_check_component.side_effect = (
        mock_health_check
    )

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

    mock_propagate_failures.return_value = results

    mock_calculate_system_health.return_value = (
        "HEALTHY"
    )

    mock_build_summary.return_value = (
        HealthSummary(
            total_components=2,
            healthy_components=2,
            failed_components=0,
            health_percentage=100.0
        )
    )

    graph_file = (
        Path("generated_graphs") 
        / "dag_test.png"
    )

    graph_file.parent.mkdir(
        exist_ok=True
    )

    graph_file.touch()

    mock_generate_graph.return_value = (
        str(graph_file)
    )

    payload = {
        "components": [
            {
                "id": "A",
                "dependencies": []
            },
            {
                "id": "B",
                "dependencies": ["A"]
            }
        ]
    }

    response = client.post(
        "/api/v1/system/health",
        json=payload
    )

    assert response.status_code == 200

    response_json = response.json()

    assert (
        response_json["overall_status"]
        == "HEALTHY"
    )

    assert(
        response_json["summary"]["total_components"] == 2
    )

    assert(
        Path(response_json["graph_file"])
        == Path("generated_graphs/dag_test.png")
    )


def test_check_health_validation_failure():
    payload = {
        "components": []
    }

    response = client.post(
        "/api/v1/system/health",
        json=payload
    )

    assert response.status_code == 400

    response_json = response.json()

    assert response_json["success"] is False



@patch("app.main.GraphVisualizer.generate_graph")
@patch("app.main.HealthAggregator.propagate_failures")
@patch("app.main.HealthChecker.check_component")
@patch("app.main.BFSTraversal.traverse")
@patch("app.main.DagBuilder.build_graph")
@patch("app.main.DagValidator.validate")
def test_generate_graph_success(
    mock_validate,
    mock_build_graph,
    mock_traverse,
    mock_check_component,
    mock_propagate_failures,
    mock_generate_graph
):
    
    mock_build_graph.return_value = {
        "A": []
    }

    mock_traverse.return_value = [
        "A"
    ]

    async def mock_health_check(component_id):
        return ComponentHealth(
            component=component_id,
            status="HEALTHY"
        )
    
    mock_check_component.side_effect = (
        mock_health_check
    )

    mock_propagate_failures.return_value = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        )
    ]

    graph_file = (
        Path("generated_graphs") 
        / "dag_test.png"
    )

    graph_file.parent.mkdir(
        exist_ok=True
    )

    graph_file.touch()

    mock_generate_graph.return_value = (
        str(graph_file)
    )

    payload = {
        "components": [
            {
                "id": "A",
                "dependencies": []
            }
        ]
    }

    response = client.post(
        "/api/v1/system/graph",
        json=payload
    )

    assert response.status_code == 200

    assert (
        response.headers["content-type"]
        == "image/png"
    )