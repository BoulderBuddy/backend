from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class ExerciseParameter(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)


class ExerciseParameterAssociation(Base):
    parameter_id = Column(ForeignKey("exerciseparameter.id"), primary_key=True)
    exercise_id = Column(ForeignKey("exercise.id"), primary_key=True)
    parameter = relationship(ExerciseParameter, backref="parameter_associations")


class Exercise(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    parameters: list[ExerciseParameter] = relationship(
        ExerciseParameter,
        secondary=ExerciseParameterAssociation.__table__,
        overlaps="parameter,parameter_associations",
    )
