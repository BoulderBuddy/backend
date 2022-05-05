from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Workout(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(String(10), ForeignKey("user.id"), nullable=True)
    user = relationship("User", back_populates="workouts")
