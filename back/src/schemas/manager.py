from pydantic.main import BaseModel


class ManagerBase(BaseModel):
	phone: str
	name: str
	is_blocked: bool = False


class ManagerInDB(ManagerBase):
	id: int
	
	class Config:
		orm_mode = True


class ManagerCreate(ManagerBase):
	pass


class Manager(ManagerInDB):
	pass
