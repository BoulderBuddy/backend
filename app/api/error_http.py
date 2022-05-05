from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.exceptions import NotFoundException


class BaseError(BaseModel):
    detail: str


class HTTPErrorNotFound(BaseError):
    class Config:
        schema_extra = {
            "example": {"detail": "Resource could not be found"},
        }


NotFoundResponse = {
    404: {"model": HTTPErrorNotFound, "description": "Resource could not be found"}
}


def add_custom_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        error_obj = HTTPErrorNotFound(detail=str(exc))
        return JSONResponse(status_code=404, content=jsonable_encoder(error_obj))
