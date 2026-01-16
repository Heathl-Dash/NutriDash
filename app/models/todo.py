from sqlalchemy import (
    Boolean, 
    Column, 
    DateTime, 
    ForeignKey, 
    Integer, 
    String, 
    func
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.db.database import Base


class ToDo(Base):
    __tablename__ = "to_dos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    done = Column(Boolean, default=False)
    keycloak_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    created = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    histories = relationship(
        "ToDohistory", back_populates="todo", cascade="all, delete-orphan"
    )


class ToDohistory(Base):
    __tablename__ = "to_do_histories"

    to_do_history_id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("to_dos.id"), nullable=False)
    keycloak_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    date_done = Column(DateTime, default=func.now())

    todo = relationship("ToDo", back_populates="histories")
