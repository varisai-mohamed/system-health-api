from unittest.mock import patch

from app.services.graph_visualizer import GraphVisualizer

from app.models.component import Component
from app.models.health_response import ComponentHealth


@patch("app.services.graph_visualizer.Digraph.render")
def test_generate_graph_success(
    mock_render
):
    components = [
        Component(id="A", dependencies=[]),
        Component(id="B", dependencies=["A"])
    ]

    health_results = [
        ComponentHealth(
            component="A",
            status="HEALTHY"
        ),
        ComponentHealth(
            component="B",
            status="FAILED"
        )
    ]

    result = GraphVisualizer.generate_graph(
        components,
        health_results
    )

    assert result.endswith(".png")

    mock_render.assert_called_once()


@patch("app.services.graph_visualizer.Digraph.render")
def test_generate_graph_empty_components(
    mock_render
):
    result = GraphVisualizer.generate_graph(
        [],
        []
    )

    assert result.endswith(".png")

    mock_render.assert_called_once()


@patch("app.services.graph_visualizer.Digraph.render")
def test_generate_graph_render_png(
    mock_render
):
    GraphVisualizer.generate_graph(
        [],
        []
    )

    _, kwargs = mock_render.call_args

    assert kwargs["format"] == "png"
    assert kwargs["cleanup"] is True


@patch("app.services.graph_visualizer.Digraph.render")
def test_generate_graph_with_failed_node(
    mock_render
):
    components = [
        Component(id="A", dependencies=[])
    ]

    health_results = [
        ComponentHealth(
            component="A",
            status="FAILED"
        )
    ]

    result = GraphVisualizer.generate_graph(
        components,
        health_results
    )

    assert result.endswith(".png")

    mock_render.assert_called_once()


@patch("app.services.graph_visualizer.Digraph.render")
def test_generate_graph_with_multiple_dependencies(
    mock_render
):
    components = [
        Component(id="A", dependencies=[]),
        Component(id="B", dependencies=["A"]),
        Component(id="C", dependencies=["A"])
    ]

    health_results = [
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
            status="HEALTHY"
        )
    ]

    result = GraphVisualizer.generate_graph(
        components,
        health_results
    )

    assert result.endswith(".png")