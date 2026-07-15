from app.services.dag_builder import DagBuilder


def test_build_graph_success(sample_components):
    graph = DagBuilder.build_graph(
        sample_components
    )

    assert graph["A"] == ["B"]
    assert graph["B"] == ["C"]


def test_build_graph_empty():
    graph = DagBuilder.build_graph([])

    assert len(graph) == 0


def test_build_graph_single_node():
    from app.models.component import Component

    graph = DagBuilder.build_graph(
        [
            Component(
                id="A",
                dependencies=[]
            )
        ]
    )

    assert len(graph) == 0


def test_build_graph_multiple_children():
    from app.models.component import Component

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
            dependencies=["A"]
        )
    ]

    graph = DagBuilder.build_graph(
        components
    )

    assert sorted(graph["A"]) == ["B", "C"]