from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
	username: Optional[str] = None
	is_admin: bool = False
	email: Optional[str] = None
	first_name: Optional[str] = None
	last_name: Optional[str] = None
	phone: Optional[str] = None
	vk_id: Optional[int] = None
	avatar_url: Optional[str] = None
	
class UserBaseInDB(UserBase):
	id: int = None

	class Config:
		orm_mode = True
		
class UserCreate(UserBase):
	username: str
	password: str
	
class User(UserBaseInDB):
	pass

