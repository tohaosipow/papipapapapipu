from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from database.session import Base
from models.base import BaseModel

admins = Table('community_admins', Base.metadata,
               Column('community_id', BigInteger, ForeignKey('community.id', ondelete='CASCADE'), nullable=False),
               Column('user_id', BigInteger, ForeignKey('user.id'), nullable=False)
               )

managers = Table('community_managers', Base.metadata,
                 Column('community_id', BigInteger, ForeignKey('community.id', ondelete='CASCADE'), nullable=False),
                 Column('manager_id', BigInteger, ForeignKey('manager.id'), nullable=False)
                 )


class Community(BaseModel, Base):
    __tablename__ = 'community'
    id = Column(BigInteger, primary_key=True)
    community_vk_id = Column(BigInteger, nullable=False)
    api_key = Column(String(100), nullable=True)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(200), nullable=True)
    admins = relationship('User', secondary=admins, back_populates='admin_communities', lazy=True)
    managers = relationship('Manager', secondary=managers, back_populates='manage_community', lazy=True)
    settings = relationship('Setting', back_populates='community', lazy=True, single_parent=True)
    calls = relationship('Call', back_populates='community', lazy=True)
