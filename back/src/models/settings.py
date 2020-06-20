from database.session import Base
from models.base import BaseModel
from sqlalchemy import BigInteger, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Setting(BaseModel, Base):
    __tablename__ = 'setting'
    id = Column(BigInteger, primary_key=True)
    welcome_speech = Column(String(1000), nullable=False)
    color_button = Column(String(6), nullable=False)
    community_id = Column(BigInteger, ForeignKey('community.id', ondelete="CASCADE"), nullable=False, unique=True)
    community = relationship("Community", lazy=True, back_populates='settings')\
