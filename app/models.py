from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Workout(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(String(10), ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="workouts")


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    workouts = relationship(
        "Workout",
        cascade="all,delete-orphan",
        back_populates="user",
        uselist=True,
    )
