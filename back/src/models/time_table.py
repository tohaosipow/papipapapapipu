from sqlalchemy import Column, BigInteger, ForeignKey, String, Time
from sqlalchemy.orm import relationship

from database.session import Base
from models.base import BaseModel


class TimeTable(BaseModel, Base):
    __tablename__ = 'time_table'
    id = Column(BigInteger, primary_key=True)
    manager_id = Column(BigInteger, ForeignKey('manager.id', ondelete="CASCADE"), nullable=False)
    day_of_the_week = Column(String(10), nullable=False)
    start_work = Column(Time, nullable=False)
    end_work = Column(Time, nullable=False)
    manager = relationship("Manager", lazy=True, back_populates='time_table')
