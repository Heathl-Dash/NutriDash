from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime, timezone
from app.db.database import Base

class WaterGoalLog(Base):
    __tablename__ = "water_goal_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    water_goal_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=True)

    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))