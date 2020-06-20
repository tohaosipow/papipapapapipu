from sqlalchemy import Column, BigInteger, Boolean, String
from sqlalchemy.orm import relationship

from database.session import Base
from models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

from models.community import admins


class User(BaseModel, Base):
	__tablename__ = 'user'
	id = Column(BigInteger, primary_key=True)
	vk_id = Column(BigInteger, nullable=True)
	is_admin = Column(Boolean, nullable=False)
	first_name = Column(String(100), nullable=True)
	last_name = Column(String(100), nullable=True)
	phone = Column(String(12), nullable=True)
	email = Column(String(100), nullable=True)
	username = Column(String(100), unique=True, nullable=False)
	password = Column(String(255), nullable=False)
	avatar_url = Column(String(200), nullable=True)
	
	admin_communities = relationship('Community', secondary=admins, back_populates='admins', lazy=True)
	calls = relationship('Call', back_populates='user', lazy=True, single_parent=True)

	
	def check_password(self, password_to_check) -> bool:
		return check_password_hash(self.password, password_to_check)

	def set_password(self, password):
		self.password = generate_password_hash(password)