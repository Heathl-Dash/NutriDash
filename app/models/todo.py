from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class ToDo(Base):
    __tablename__ = "to_dos"
    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    done = Column(Boolean, default=False)

    histories = relationship("ToDohistory", back_populates="todo", cascade="all, delete-orphan")

class ToDohistory(Base):
    __tablename__ = "to_do_histories"
    to_do_history_id = Column(Integer, primary_key=True, index=True)
    todo_id = Column(Integer, ForeignKey("to_dos.todo_id"), nullable=False)
    date_done = Column(Date, default=func.current_date())

    todo = relationship("ToDo", back_populates="histories")