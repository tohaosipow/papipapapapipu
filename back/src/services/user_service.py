from typing import Optional

from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models.user import User
from schemas.users import UserCreate


class UserService:
	def get_by_username(self, db_session: Session, username: str) -> User:
		user = db_session.query(User).filter_by(username=username).first()
		return user
	
	def get_user_by_id(self, db_session: Session, user_id: int):
		user =  db_session.query(User).options(lazyload('admin_communities')).get(user_id)
		if user is None:
			raise NoResultFound('User not found')
		return user
		
	def create_user(self, db_session: Session, user_to_create: UserCreate):
		existing_user = self.get_by_username(db_session, user_to_create.username)
		if existing_user is not None:
			raise Exception('User already exists')
		
		new_user = User(
			username=user_to_create.username,
			first_name=user_to_create.first_name,
			last_name=user_to_create.last_name,
			is_admin=user_to_create.is_admin,
			vk_id=user_to_create.vk_id,
			avatar_url=user_to_create.avatar_url,
			email=user_to_create.email,
			phone=user_to_create.phone,
			password=user_to_create.password,
		)

		new_user.set_password(user_to_create.password)
		db_session.add(new_user)
		db_session.commit()
		db_session.refresh(new_user)
		return new_user
	
	def check_password(self, db_session: Session, username: str, password: str) -> Optional[User]:
		user_to_check = self.get_by_username(db_session, username=username)
		if not user_to_check:
			return None
		if not user_to_check.check_password(password):
			return None
		return user_to_check
	
	def get_communities(self, db_session: Session, user_id: int):
		user = db_session.query(User).options(lazyload('admin_communities')).filter_by(id=user_id).first()
		return user.admin_communities

user = UserService()