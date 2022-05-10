from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.db.database import Base


class ExerciseParameter(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    unit_type = Column(String(256), nullable=False)


class ExerciseParameterAssociation(Base):
    parameter_id = Column(ForeignKey("exerciseparameter.id"), primary_key=True)
    exercise_id = Column(ForeignKey("exercise.id"), primary_key=True)
    parameter = relationship(ExerciseParameter)


class Exercise(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    _parameters = relationship(
        ExerciseParameterAssociation,
        lazy="joined",
        cascade="save-update, merge, delete, delete-orphan",
    )
    parameters = association_proxy(
        "_parameters",
        "parameter",
        creator=lambda _ep: ExerciseParameterAssociation(parameter=_ep),
    )
