from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import Base, KeyType

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: KeyType) -> ModelType | None:
        return db.query(self.model).get(id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        return self.save(db, db_obj=db_obj)

    def save(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for key, value in update_data.items():  # TODO probably very insecure
            setattr(db_obj, key, value)

        return self.save(db, db_obj=db_obj)

    def remove(self, db: Session, *, id: KeyType) -> ModelType | None:
        obj = self.get(db, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
