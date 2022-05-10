import json
import pathlib
from typing import Any, Callable, Dict, Generic, TypeVar, get_args

from jsonschema import RefResolver, validate
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.database import Base


class TestSchemas:
    USER: str = "User.json"
    USER_LIST: str = "UserList.json"
    EXERCISE_PARAMETER: str = "ExerciseParameter.json"
    EXERCISE_PARAMETER_LIST: str = "ExerciseParameterList.json"
    EXERCISE: str = "Exercise.json"
    EXERCISE_LIST: str = "ExerciseList.json"


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
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
CRUDType = TypeVar("CRUDType", bound=CRUDBase)


class CRUDTestUtil(Generic[CRUDType, ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, default_data: CreateSchemaType | Dict[str, Any], crud: CRUDType):
        self.default_data = default_data
        self.crud = crud
        self.create = get_args(crud.__orig_bases__[0])[1]
        self.update = get_args(crud.__orig_bases__[0])[2]

    def insert_into_db(
        self, db: Session, data: CreateSchemaType | Dict[str, Any] | None = None
    ) -> ModelType:
        obj_in = data or self.default_data
        if isinstance(obj_in, dict):
            obj_in = self.create(**obj_in)
        return self.crud.create(db, obj_in=obj_in)

    def update_into_db(
        self, db: Session, db_obj: ModelType, data: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        obj_in = data or self.default_data
        if isinstance(obj_in, dict):
            obj_in = self.update(**obj_in)
        return self.crud.update(db, db_obj=db_obj, obj_in=obj_in)

    def create_assert(
        self,
        db: Session,
        data: CreateSchemaType | Dict[str, Any],
        *,
        db_obj_map: Callable[[ModelType], Dict[str, Any]] | None = None,
    ) -> None:
        db_obj = self.insert_into_db(db, data)

        if db_obj_map:
            db_obj_dict = db_obj_map(db_obj)
        else:
            db_obj_dict = db_obj.__dict__

        if isinstance(data, self.create):
            data = data.dict(exclude_unset=True)

        assert db_obj is not None
        assert data.items() <= db_obj_dict.items()
