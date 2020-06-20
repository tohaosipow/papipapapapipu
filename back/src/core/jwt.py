import time
from datetime import datetime, timedelta

import jwt

from core import config

ALGORITHM = "HS256"
EXPIRE_TIME_IN_SECONDS = 60 * 60


def create_access_token(*, data: dict):
	to_encode = data.copy()
	creation_time = time.time()
	expire = int(time.time() + EXPIRE_TIME_IN_SECONDS)
	to_encode.update({"expire_time": expire, "creation_time": creation_time})
	encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def create_refresh_token(*, data: dict):
	to_encode = data.copy()
	encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt
