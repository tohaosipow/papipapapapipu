from datetime import timezone
from typing import List

import requests
from api.utils.security import get_current_user_by_access_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from starlette import status

import services
from api.utils.db import get_db
from database.session import Session
from schemas.call import CallCreate, Call
from models.user import User as UserDomain
router = APIRouter()


@router.get('/getCall/{call_id}', response_model=Call)
def get_call(
		call_id: int,
		db: Session = Depends(get_db)
):
	try:
		call = services.call.get(db, call_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return call


@router.get('/getCallHistory/{community_id}', response_model=List[Call])
def get_call_history(
		community_id: int,
		db: Session = Depends(get_db)
):
	try:
		calls = services.call.get_call_history(db, community_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	for call in calls:
		if call.hidden == True:
			call.client_phone = None
	return calls


@router.post('/create_call/communities/{community_id}')
def create_call(
		community_id: int,
		call_to_create: CallCreate,
		current_user: UserDomain = Depends(get_current_user_by_access_token),
		db: Session = Depends(get_db)
):
	try:
		call = services.call.create(db, call_to_create, community_id, current_user.id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	rq = services.call.get_call_asterisk(db, call.id)
	params = {'client_phone': rq.user_phone,
			  'client_name': rq.user_name,
			  'manager_name': rq.manager_name,
			  'manager_phone': rq.manager_phone,
			  'community_name': rq.community_name,
			  'timestamp': int(rq.call_time.timestamp())}
	requests.get('https://asterisk.dotsolution.org/call.php',
				 params=params, )
	return params


@router.delete('/delete/{call_id}')
def delete_call(
		call_id: int,
		db: Session = Depends(get_db)
):
	try:
		call = services.call.remove(db, call_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return {'id': call_id}
