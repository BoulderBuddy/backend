from enum import Enum as EnumClass

from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer
from sqlalchemy.orm import relationship

from app.db import CustomEnum, CustomNumeric, KeyType
from app.db.database import Base

from .exercise import Exercise, ExerciseParameter


class SetStatus(EnumClass):
    PLANNED = 0
    PARTIAL = 1
    COMPLETE = 2


class ExerciseParameterValue(Base):
    exercise_id: KeyType = Column(ForeignKey(Exercise.id), primary_key=True)
    parameter_id: KeyType = Column(ForeignKey(ExerciseParameter.id), primary_key=True)
    set_index: int = Column(
        ForeignKey("set.index"),
        primary_key=True,
    )
    workout_id: KeyType = Column(ForeignKey("workout.id"), primary_key=True)

    parameter = relationship(ExerciseParameter)
    exercise = relationship(Exercise)
    set = relationship("Set", back_populates="values")
    workout = relationship("Workout")

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

    values: list[ExerciseParameterValue] = relationship(
        ExerciseParameterValue,
        primaryjoin="and_(ExerciseParameterValue.set_index == Set.index, Set.workout_id == ExerciseParameterValue.workout_id, Set.exercise_id == ExerciseParameterValue.exercise_id)",  # noqa
        cascade="all, delete-orphan",
    )
    exercise_set = relationship("ExerciseSet", back_populates="sets")

    status: SetStatus = Column(CustomEnum(SetStatus))


class ExerciseSet(Base):
    workout_id = Column(Integer, ForeignKey("workout.id"), primary_key=True)
    exercise_id = Column(Integer, ForeignKey(Exercise.id), primary_key=True)
    exercise: Exercise = relationship(Exercise)

    sets: list[Set] = relationship(Set, cascade="all, delete-orphan")


class Workout(Base):
    id = Column(Integer, primary_key=True, index=True)
    exercises: list[ExerciseSet] = relationship(
        ExerciseSet, cascade="all, delete-orphan"
    )

    training_id = Column(
        Integer, ForeignKey("trainingsession.id"), nullable=True
    )  # TODO maybe change into FALSE
    # training = relationship("TrainingSession")
