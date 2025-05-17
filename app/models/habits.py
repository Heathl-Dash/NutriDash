from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class Habit(Base):
    __tablename__ = "habits"

    habit_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    positive = Column(Boolean, default=False)
    negative = Column(Boolean, default=False)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)