from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from database.session import Base
from models.base import BaseModel
from models.community import managers


class Manager(BaseModel, Base):
	__tablename__ = 'manager'
	id = Column(BigInteger, primary_key=True)
	phone = Column(String(12), nullable=False)
	name = Column(String(100), nullable=False)
	is_blocked = Column(Boolean, nullable=False)
	manage_community = relationship('Community', lazy=True, secondary=managers, back_populates='managers')
	calls = relationship('Call', back_populates='manager', lazy=True, single_parent=True)
	time_table = relationship('TimeTable', lazy=True, back_populates='manager')
