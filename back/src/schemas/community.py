from typing import List

from pydantic.main import BaseModel

from schemas.manager import ManagerCreate, Manager
from schemas.users import User


class CommunityBase(BaseModel):
	community_vk_id: int
	name: str
	avatar_url: str
	admins: List[User]
	managers: List[ManagerCreate]
	
class CommunityInDB(CommunityBase):
	id: int
	
	class Config:
		orm_mode = True

class CommunityCreate(BaseModel):
	community_vk_id: int
	name: str
	avatar_url: str
	admins: List[int]
	managers: List[ManagerCreate]
	
class Community(CommunityInDB):
	admins: List[User]
	managers: List[Manager]