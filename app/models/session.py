from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base

from .user import User
from .workout import Workout


class TrainingSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    user = relationship(User, back_populates="sessions")
    workouts: list[Workout] = relationship(Workout)
