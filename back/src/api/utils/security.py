import string
from base64 import b64encode
import time
from hashlib import sha256
from collections import OrderedDict
from hmac import HMAC
import random
from urllib.parse import urlencode
import services
import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from api.utils.db import get_db
from core import config
from core.jwt import ALGORITHM
from database.session import Session
from schemas.token import AccessTokenPayload, RefreshTokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


def get_current_user_by_access_token(db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	try:
		payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
		token_data = AccessTokenPayload(**payload)
	except PyJWTError:
		raise HTTPException(
			status_code=HTTP_403_FORBIDDEN, detail="Credentials are invalid"
		)
	if int(time.time()) > token_data.expire_time:
		raise HTTPException(
			status_code=HTTP_401_UNAUTHORIZED, detail="Access Token is expired"
		)
	user = services.user.get_user_by_id(db_session, user_id=token_data.user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user


def get_current_user_by_refresh_token(db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
	try:
		payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM], verify=False)
		token_data = RefreshTokenPayload(**payload)
	except PyJWTError:
		raise HTTPException(
			status_code=HTTP_403_FORBIDDEN, detail="Credentials are invalid"
		)
	user = services.user.get_user_by_id(db_session, user_id=token_data.user_id)
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user


def is_vk_sign_valid(*, query: dict, secret: str) -> bool:
	"""Check VK Apps signature"""
	vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
	hash_code = b64encode(HMAC(secret.encode(), urlencode(vk_subset, doseq=True).encode(), sha256).digest())
	decoded_hash_code = hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')
	return query["sign"] == decoded_hash_code


def random_string():
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
