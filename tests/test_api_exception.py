from app.exceptions.api_exception import ApiException


def test_api_exception_properties():

    exception = ApiException(
        status_code=400,
        message="Validation Error"
    )

    assert exception.status_code == 400
    assert exception.message == "Validation Error"


def test_api_exception_is_exception():

    exception = ApiException(
        status_code=500,
        message="Internal Server Error"
    )

    assert isinstance(
        exception,
        Exception
    )


def test_api_exception_string_representation():

    exception = ApiException(
        status_code=400,
        message="Not Found"
    )

    assert str(exception) == "Not Found"