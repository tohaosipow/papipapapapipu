from sqlalchemy import Column, DateTime, func

class BaseModel(object):
	updated_at = Column(
		DateTime,
		server_default=func.now(),
		server_onupdate=func.now()
	)
	created_at = Column(
		DateTime,
		server_default=func.now(),
	)