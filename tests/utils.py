import json
import pathlib
from typing import Any, Dict, Type, TypeVar

from jsonschema import RefResolver, validate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.database import Base


class TestSchemas:
    USER: str = "User.json"
    USER_LIST: str = "UserList.json"


def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/schemas")
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema,  # it's used to resolve the file inside schemas correctly
        ),
    )


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)


def insert_into_db_template(
    model: Type[ModelType],
    create: Type[CreateSchemaType],
    crud: CRUDType,
    default_data: Dict[str, Any],
):
    def inner_func(db: Session, data: Dict[str, Any] | None = None) -> model:
        if data is None:
            data = default_data

        obj_in = create(**data)
        return crud.create(db, obj_in=obj_in)

    return inner_func
