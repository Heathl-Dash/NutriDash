from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.db.database import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    positive = Column(Boolean, default=False)
    negative = Column(Boolean, default=False)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    user_id = Column(Integer, nullable=False)
    created = Column(DateTime, default=func.now(), nullable=False)
