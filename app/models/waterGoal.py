from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    ForeignKey, 
    DateTime, 
    func, 
    text
)
from sqlalchemy.orm import relationship
from app.db.database import Base

class WaterGoal(Base):
    __tablename__ = "water_goals"
    water_goal_id = Column(Integer, primary_key=True, index=True)
    ml_goal = Column(Integer, nullable=False)
    ml_drinked = Column(Integer, default=0)
    user_id = Column(Integer, nullable=False)
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False
)

    bottles = relationship("WaterBottle", back_populates="goal", cascade="all, delete-orphan")

class WaterBottle(Base):
    __tablename__ = "water_bottles"
    water_bottle_id = Column(Integer, primary_key=True, index=True)
    water_goal_id = Column(Integer, ForeignKey("water_goals.water_goal_id"), nullable=False)
    bottle_name = Column(String, nullable=False)
    ml_bottle = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    id_bottle_style = Column(
        Integer, 
        nullable=False, 
        default=1, 
        server_default=text("1")
    )


    goal = relationship("WaterGoal", back_populates="bottles")


class WaterIntake(Base):
    __tablename__= "water_intakes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    water_goal_id = Column(
        Integer, 
        ForeignKey("water_goals.water_goal_id"),
        nullable=False
    )
    water_bottle_id = Column(
        Integer, 
        ForeignKey("water_bottles.water_bottle_id"), 
        nullable=False
    )
    ml = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    goal = relationship("WaterGoal", backref="intakes")
    bottle = relationship("WaterBottle")