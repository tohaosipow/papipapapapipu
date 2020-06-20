from sqlalchemy import Column, BigInteger, ForeignKey, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship

from database.session import Base
from models.base import BaseModel


class Call(BaseModel, Base):
	__tablename__ = 'call'
	id = Column(BigInteger, primary_key=True)
	community_id = Column(BigInteger, ForeignKey('community.id', ondelete="CASCADE"), nullable=False)
	client_phone = Column(String(12), nullable=True)
	hidden = Column(Boolean, nullable=False)
	answered = Column(Boolean, nullable=False)
	call_time = Column(DateTime, nullable=False)
	rate = Column(Integer, nullable=True)
	result = Column(String(1000), nullable=True)
	manager_id = Column(BigInteger, ForeignKey('manager.id', ondelete="SET NULL"), nullable=True)
	community = relationship("Community", lazy=True, back_populates='calls')
	manager = relationship("Manager", lazy=True, back_populates='calls')
	user_id = Column(BigInteger, ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
	user = relationship("User", lazy=True, back_populates='calls')
