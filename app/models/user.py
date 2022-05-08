from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    sessions = relationship(
        "TrainingSession",
        cascade="all,delete-orphan",
        back_populates="user",
        uselist=True,
    )
