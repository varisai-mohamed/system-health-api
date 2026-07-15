from unittest.mock import patch
import pytest

from app.services.health_checker import HealthChecker

@pytest.mark.asyncio
@patch("app.services.health_checker.asyncio.sleep")
@patch("app.services.health_checker.random.choice")
async def test_check_component_healthy(
    mock_choice,
    mock_sleep
):
    mock_choice.return_value = "HEALTHY"

    result = await HealthChecker.check_component("A")

    assert result.component == "A"
    assert result.status == "HEALTHY"

    mock_sleep.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.health_checker.asyncio.sleep")
@patch("app.services.health_checker.random.choice")
async def test_check_component_failed(
    mock_choice,
    mock_sleep
):
    mock_choice.return_value = "FAILED"

    result = await HealthChecker.check_component("A")

    assert result.component == "A"
    assert result.status == "FAILED"

    mock_sleep.assert_called_once()


@pytest.mark.asyncio
@patch("app.services.health_checker.asyncio.sleep")
@patch("app.services.health_checker.random.choice")
async def test_check_component_calls_random_choice(
    mock_choice,
    mock_sleep
):
    mock_choice.return_value = "HEALTHY"

    await HealthChecker.check_component("COMP1")

    mock_choice.assert_called_once_with(
        ["HEALTHY", "HEALTHY", "FAILED"]
    )