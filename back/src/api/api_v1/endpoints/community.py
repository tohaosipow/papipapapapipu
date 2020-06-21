from typing import List

from core import config

from api.utils.security import get_current_user_by_access_token
from sqlalchemy.orm.exc import NoResultFound
from starlette import status
from starlette.exceptions import HTTPException

from api.utils.db import get_db
from fastapi import APIRouter, Depends

import services
from database.session import Session
from schemas.community import CommunityCreate, Community
from schemas.manager import ManagerCreate, Manager
from models.user import User as UserDomain

router = APIRouter()


@router.post('/create', response_model=Community)
def create_community(
		community_to_create: CommunityCreate,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	try:
		community = services.community.create(db, community_to_create, current_user.id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
	return community


@router.delete('/delete/{community_id}', response_model=Community)
def delete_community(
		community_id: int,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	try:
		is_admin = services.community.is_current_user_admin(db, current_user.id, community_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

	if not is_admin:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.USER_IS_NOT_ADMIN)

	try:
		community = services.community.remove(db, community_id, current_user.id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return community


@router.get('/getCommunity/{community_id}', response_model=Community)
def get_community(
		community_id: int,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	try:
		is_admin = services.community.is_current_user_admin(db, current_user.id, community_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	if not is_admin:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.USER_IS_NOT_ADMIN)
	try:
		community = services.community.get(db, community_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return community


@router.get('/getCommunityByVkId/{community_vk_id}', response_model=Community)
def get_community(
		community_vk_id: int,
		db: Session = Depends(get_db)
):
	try:
		community = services.community.get_by_vk_id(db, community_vk_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

	return community


@router.put('/addManager/{community_id}', response_model=Community)
def add_manager(
		community_id: int,
		manager_to_add: ManagerCreate,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	if manager_to_add is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

	try:
		is_admin = services.community.is_current_user_admin(db, current_user.id, community_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	if not is_admin:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.USER_IS_NOT_ADMIN)
	try:
		manager = services.community.add_manager(db, community_id, manager_to_add)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return manager


@router.put('/removeManager/{community_id}/managers/{manager_id}', response_model=Manager)
def remove_manager(
		community_id: int,
		manager_id: int,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	try:
		is_admin = services.community.is_current_user_admin(db, current_user.id, community_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	if not is_admin:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.USER_IS_NOT_ADMIN)
	try:
		services.community.get(db, community_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

	try:
		manager = services.community.remove_manager(db, manager_id)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return manager
