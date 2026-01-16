from datetime import datetime, timezone
from sqlalchemy import JSON, Column, DateTime, Integer, String
from app.db.database import Base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class WaterGoalLog(Base):
    __tablename__ = "water_goal_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)
    water_goal_id = Column(Integer, nullable=False)
    keycloak_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)

    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
