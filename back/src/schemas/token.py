from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str


class AccessTokenPayload(BaseModel):
	user_id: int = None
	username: str = None
	creation_time: int = None
	expire_time: int = None


class RefreshTokenPayload(BaseModel):
	user_id: int = None
	username: str = None
