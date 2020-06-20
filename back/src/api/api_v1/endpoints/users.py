from typing import Optional, List
from urllib.parse import parse_qsl

from fastapi.security import OAuth2PasswordRequestForm

from core.jwt import create_access_token, create_refresh_token

from core import config

import services
from api.utils.security import is_vk_sign_valid, random_string, get_current_user_by_access_token, \
    get_current_user_by_refresh_token
from schemas.community import Community

from schemas.token import Token
from starlette.requests import Request

from api.utils.db import get_db
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from models.user import User as UserDomain
from database.session import Session
from schemas.users import UserCreate, User

router = APIRouter()


@router.get('/', response_model=User)
def get_current_user(current_user: UserDomain = Depends(get_current_user_by_access_token)):
	return current_user

@router.get('/getUserCommunities', response_model=List[Community])
def get_user_communities(
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	return services.user.get_communities(db, current_user.id)

@router.post('/token', response_model=Token)
async def login(
		form_data: OAuth2PasswordRequestForm = Depends(),
		db: Session = Depends(get_db)
):
	user = services.user.check_password(db, form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(
		data={"username": user.username, "user_id": user.id}
	)
	refresh_token = create_refresh_token(
		data={"username": user.username, "user_id": user.id}
	)
	return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post('/authByVk', response_model=Token)
def auth_by_vk(
		vk_access_token_settings: Optional[str],
		vk_app_id: Optional[int],
		vk_are_notifications_enabled: Optional[int],
		vk_is_app_user: Optional[int],
		vk_is_favorite: Optional[int],
		vk_language: Optional[str],
		vk_platform: Optional[str],
		vk_ref: Optional[str],
		vk_user_id: Optional[int],
		sign: Optional[str],
		request: Request,
		referrer_id: Optional[int] = None,
		db: Session = Depends(get_db)
):
	"""
	Authenticate user from vk app.
	"""

	query = dict(parse_qsl(request.url.query, keep_blank_values=True))

	is_secret_valid = is_vk_sign_valid(query=query, secret=config.VK_APP_SECRET)
	if not is_secret_valid:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Vk sign is invalid",
			headers={"WWW-Authenticate": "Bearer"},
		)

	vk_id = request.query_params.get('vk_user_id')
	vk_user = services.vk_service.get_user_by_id(vk_id)
	if vk_user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Vk user id is invalid",
		)

	username = request.query_params.get('username') or vk_id
	user = services.user.get_by_username(db, username)
	if user is None:
		user_to_create: UserCreate = UserCreate(
			username=vk_id,
			first_name=vk_user['first_name'],
			last_name=vk_user['last_name'],
			is_admin=False,
			vk_id=vk_id,
			avatar_url=vk_user['photo_50'],
			password=random_string()
		)
		user = services.user.create_user(db, user_to_create)

	access_token = create_access_token(
		data={"username": user.username, "user_id": user.id}
	)
	refresh_token = create_refresh_token(
		data={"username": user.username, "user_id": user.id}
	)
	return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", }


@router.post('/createUser', response_model=User)
def create_user(
		user_to_create: UserCreate,
		db: Session = Depends(get_db)
):
	if user_to_create is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
	try:
		user = services.user.create_user(db, user_to_create)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=str(e),
		)
	return user

@router.post('/refresh', response_model=Token)
async def refresh(request: Request, db: Session = Depends(get_db)):
	refresh_token = request.headers.get('refresh-token')
	print(refresh_token)
	if refresh_token is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	user = get_current_user_by_refresh_token(db_session=db, token=refresh_token)
	access_token = create_access_token(
		data={"username": user.username, "user_id": user.id}
	)
	return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/test_ci')
def test():
	return 'OK'