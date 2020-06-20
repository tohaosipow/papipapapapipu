from typing import List

from sqlalchemy.orm.exc import NoResultFound
from starlette import status

import services
from api.utils.db import get_db
from fastapi import APIRouter, Depends, HTTPException

from database.session import Session

from schemas.call import CallCreate, Call, CallAsterisk

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


@router.post('/create_call/communities/{community_id}', response_model=Call)
def create_call(
		community_id: int,
		call_to_create: CallCreate,
		db: Session = Depends(get_db)
):
	try:
		call = services.call.create(db, call_to_create, community_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return call


@router.get('/getCallAsterisk/{call_id}', response_model=CallAsterisk)
def get_call_asterisk(
		call_id: int,
		db: Session = Depends(get_db)
):
	try:
		call_asterisk = services.call.get_call_asterisk(db, call_id)
	except NoResultFound as e:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
	return call_asterisk
