from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.api_exception import ApiException
from app.utils.logger import logger


def register_exception_handlers(
        app:FastAPI
):
    
    @app.exception_handler(ApiException)
    async def api_exception_handler(
        request: Request,
        exc: ApiException
    ):
        
        logger.error(exc.message)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message
            }
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        
        logger.exception(
            f"Unexpected error: {str(exc)}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error"
            }
        )