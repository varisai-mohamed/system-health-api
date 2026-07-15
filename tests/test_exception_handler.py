from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.exceptions.api_exception import ApiException
from app.exceptions.exception_handler import (
    register_exception_handlers
)


def create_test_app():

    app = FastAPI()

    register_exception_handlers(app)

    @app.get("/api-error")
    async def api_error():
        raise ApiException(
            status_code=400,
            message="Validation Error"
        )
    
    @app.get("/server-error")
    async def server_error():
        raise Exception(
            "Unexpected Error"
        )

    return app


def test_api_exception_handler():

    app = create_test_app()

    client = TestClient(app)

    response = client.get("/api-error")

    assert response.status_code == 400

    response_json = response.json()

    assert response_json["success"] is False
    assert response_json["error"] == "Validation Error"


def test_global_exception_handler():

    app = create_test_app()

    client = TestClient(
        app,
        raise_server_exceptions=False
    )

    response = client.get("/server-error")

    assert response.status_code == 500

    response_json = response.json()

    assert response_json["success"] is False
    assert (
        response_json["error"] == "Internal Server Error"
    )