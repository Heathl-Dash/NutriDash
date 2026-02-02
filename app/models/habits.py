from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

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
    keycloak_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
