from app.services.bfs_traversal import BFSTraversal


def test_bfs_traversal_linear_graph():
    graph = {
        "A": ["B"],
        "B": ["C"],
        "C": []
    }

    result = BFSTraversal.traverse(
        graph,
        ["A"]
    )

    assert result == ["A", "B", "C"]


def test_bfs_traversal_multiple_children():
    graph = {
        "A": ["B", "C"],
        "B": [],
        "C": []
    }

    result = BFSTraversal.traverse(
        graph,
        ["A"]
    )

    assert result == ["A", "B", "C"]


def test_bfs_traversal_multiple_root_nodes():
    graph = {
        "A": ["C"],
        "B": ["D"],
        "C": [],
        "D": []
    }

    result = BFSTraversal.traverse(
        graph,
        ["A", "B"]
    )

    assert result == ["A", "B", "C", "D"]


def test_bfs_traversal_empty_graph():
    result = BFSTraversal.traverse(
        {},
        []
    )

    assert result == []


def test_bfs_traversal_duplicate_child():
    graph = {
        "A": ["B", "B"],
        "B": []
    }

    result = BFSTraversal.traverse(
        graph,
        ["A"]
    )

    assert result == ["A", "B"]


def test_bfs_traversal_start_node_not_in_graph():
    graph = {}

    result = BFSTraversal.traverse(
        graph,
        ["A"]
    )

    assert result == ["A"]


