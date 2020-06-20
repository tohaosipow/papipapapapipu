from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class CallBase(BaseModel):
	community_id: int
	manager_id: int
	user_id: int
	
class CallInDB(CallBase):
	id: int
	
	class Config:
		orm_mode = True

class CallCreate(BaseModel):
	client_phone: Optional[str] = ''
	manager_id: int
	user_id: int
	hidden: bool
	call_time: Optional[datetime] = None


class Call(BaseModel):
	id: int
	community_id: int
	manager_phone: str
	client_phone: Optional[str] = None
	hidden: bool
	answered: bool
	
	class Config:
		orm_mode = True


class CallAsterisk(BaseModel):
	id: int
	community_name: str
	manager_name: str
	manager_phone: str
	user_name: str
	user_phone: str
	call_time: datetime
