from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic.error_wrappers import ErrorWrapper

from app.core.exceptions import AlreadyExistsException, NotFoundException


class BaseError(BaseModel):
    detail: str


class HTTPErrorNotFound(BaseError):
    class Config:
        schema_extra = {
            "example": {"detail": "Resource could not be found"},
        }


class HTTPErrorAlreadyExists(BaseError):
    identifier: Any

    class Config:
        schema_extra = {
            "example": {"detail": "Resource already exists", "identifier": "42"}
        }


def get_field_name(obj: object, field):
    gert = obj.__dict__
    return [x for (x, y) in gert.items() if y == field].pop()


def custom_validation_error(err: ValueError | str, obj, field_value, *, req_loc="body"):
    if isinstance(err, str):
        err = ValueError(err)

    param_name = get_field_name(obj, field_value)
    return [ErrorWrapper(err, (req_loc, param_name))]


def add_custom_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        error_obj = HTTPErrorNotFound(detail=str(exc))
        return JSONResponse(status_code=404, content=jsonable_encoder(error_obj))

    @app.exception_handler(AlreadyExistsException)
    async def already_exists_exception_handler(
        request: Request, exc: AlreadyExistsException
    ):
        error_obj = HTTPErrorAlreadyExists(
            detail=exc.message, identifier=exc.resource_id
        )
        return JSONResponse(status_code=400, content=jsonable_encoder(error_obj))
