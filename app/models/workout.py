from sqlalchemy import Column, Enum, ForeignKey, ForeignKeyConstraint, Integer
from sqlalchemy.orm import relationship

from app.db import CustomNumeric, KeyType
from app.db.database import Base
from app.types import SetStatus

from .exercise import Exercise, ExerciseParameter


class ExerciseParameterValue(Base):
    exercise_id: KeyType = Column(ForeignKey(Exercise.id), primary_key=True)
    parameter_id: KeyType = Column(ForeignKey(ExerciseParameter.id), primary_key=True)
    set_index: int = Column(ForeignKey("set.index"), primary_key=True)

    parameter = relationship(ExerciseParameter)
    exercise = relationship(Exercise)

    value = Column(CustomNumeric(scale=2), nullable=False)
    planned_value = Column(CustomNumeric(scale=2), nullable=True)


class Set(Base):
    __table_args__ = (
        (
            ForeignKeyConstraint(
                ["workout_id", "exercise_id"],
                [
                    "exerciseset.workout_id",
                    "exerciseset.exercise_id",
                ],
            )
        ),
    )
    index: int = Column(Integer, primary_key=True, nullable=False)

    workout_id: KeyType = Column(Integer, primary_key=True, nullable=False)
    exercise_id: KeyType = Column(Integer, primary_key=True, nullable=False)

    values: list[ExerciseParameterValue] = relationship(ExerciseParameterValue)

    status: SetStatus = Column(Enum(SetStatus))


class ExerciseSet(Base):
    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True)
    exercise_id = Column(Integer, ForeignKey(Exercise.id), primary_key=True)
    exercise = relationship(Exercise)

    sets = relationship(Set)


class Workout(Base):
    id = Column(Integer, primary_key=True, index=True)
    exercises = relationship(ExerciseSet)

    training_id = Column(
        Integer, ForeignKey("trainingsession.id"), nullable=True
    )  # TODO maybe change into FALSE
    # training = relationship("TrainingSession")
