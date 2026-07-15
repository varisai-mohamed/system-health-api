import pytest

from app.validators.dag_validator import DagValidator
from app.exceptions.api_exception import ApiException
from app.models.component import (
    Component,
    HealthCheckRequest
)


def test_validate_success():
    request= HealthCheckRequest(
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

    DagValidator.validate(request)


def test_validate_components_exist_failure():
    request = HealthCheckRequest(
        components=[]
    )

    with pytest.raises(ApiException) as exc:
        DagValidator.validate_components_exist(
            request
        )
    
    assert exc.value.status_code == 400
    assert "At least one component is required" in exc.value.message


def test_validate_duplicate_ids_failure():
    request = HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=[]
            ),
            Component(
                id="A",
                dependencies=[]
            )
        ]
    )

    with pytest.raises(ApiException) as exc:
        DagValidator.validate_unique_ids(
            request
        )

    assert exc.value.status_code == 400
    assert "Duplicate component IDs detected" in exc.value.message


def test_validate_missing_dependency_failure():
    request = HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=["X"]
            )
        ]
    )

    with pytest.raises(ApiException) as exc:
        DagValidator.validate_dependencies_exist(
            request
        )

    assert exc.value.status_code == 400
    assert "Dependency 'X' not found" in exc.value.message


def test_validate_self_dependency_failure():
    request = HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=["A"]
            )
        ]
    )

    with pytest.raises(ApiException) as exc:
        DagValidator.validate_self_dependency(
            request
        )

    assert exc.value.status_code == 400
    assert "Self dependency detected" in exc.value.message



def test_validate_circular_dependency_failure():
    request = HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=["C"]
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

    with pytest.raises(ApiException) as exc:
        DagValidator.validate_cycle(
            request
        )

    assert exc.value.status_code == 400
    assert "Circular dependency detected" in exc.value.message


def test_validate_full_validation_failure():
    request = HealthCheckRequest(
        components=[
            Component(
                id="A",
                dependencies=[]
            ),
            Component(
                id="A",
                dependencies=[]
            )
        ]
    )

    with pytest.raises(ApiException) as exc:
        DagValidator.validate(
            request
        )
