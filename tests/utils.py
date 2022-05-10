import json
import pathlib
from typing import Any, Callable, Dict, Generic, TypeVar, get_args

from jsonschema import RefResolver, validate
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
CRUDType = TypeVar("CRUDType", bound=CRUDBase)


class CRUDTestUtil(Generic[CRUDType, ModelType]):
    def __init__(self, default_data: Dict[str, Any], crud: CRUDType):
        self.default_data = default_data
        self.crud = crud
        self.create = get_args(crud.__orig_bases__[0])[1]
        self.update = get_args(crud.__orig_bases__[0])[2]

    def insert_into_db(
        self, db: Session, data: Dict[str, Any] | None = None
    ) -> ModelType:
        if data is None:
            data = self.default_data

        obj_in = self.create(**data)
        return self.crud.create(db, obj_in=obj_in)

    def update_into_db(
        self, db: Session, db_obj: ModelType, data: Dict[str, Any]
    ) -> ModelType:
        obj_in = self.update(**data)
        return self.crud.update(db, db_obj=db_obj, obj_in=obj_in)

    def create_assert(
        self,
        db: Session,
        data: Dict[str, Any],
        *,
        db_obj_map: Callable[[Any], Dict[str, Any]] | None = None,
    ) -> None:
        db_obj = self.insert_into_db(db, data)

        if db_obj_map:
            db_obj_dict = db_obj_map(db_obj)
        else:
            db_obj_dict = db_obj.__dict__

        assert db_obj is not None
        assert data.items() <= db_obj_dict.items()
