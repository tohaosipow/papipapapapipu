from datetime import datetime

from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models import Call, Community, Manager, User
from schemas.call import CallCreate, CallAsterisk
from schemas.call import Call as CallSchema


class CallService:
	def create(self, db_session: Session, call_to_create: CallCreate, community_id: int):
		community = db_session.query(Community).get(community_id)
		if community is None:
			raise NoResultFound('Community not found')
		
		manager = db_session.query(Manager).get(call_to_create.manager_id)
		if manager is None:
			raise NoResultFound('Manager not found')
		
		user = db_session.query(User).get(call_to_create.user_id)
		if user is None:
			raise NoResultFound('User not found')
			
		call = Call(
			community_id=community_id,
			client_phone=call_to_create.client_phone,
			hidden=call_to_create.hidden,
			answered=False,
			manager_id=call_to_create.manager_id,
			user_id=call_to_create.user_id,
			call_time=datetime.now() if call_to_create.call_time is None else call_to_create.call_time
		)
		
		db_session.add(call)
		db_session.commit()
		db_session.refresh(call)
		
		return CallSchema(
			id = call.id,
			community_id=community_id,
			manager_phone=manager.phone,
			client_phone=user.phone,
			answered=call.answered,
			hidden=call.hidden,
		)
	
	def get_call_history(self, db_session: Session, community_id: int):
		community = db_session.query(Community).get(community_id)
		if community is None:
			raise NoResultFound('Community not found')
		
		calls = db_session.query(Call).options(lazyload('manager'), lazyload('user')).filter_by(community_id=community_id).all()
		calls_schemas = [CallSchema(
			id=call.id,
			community_id=community_id,
			manager_phone=call.manager.phone,
			client_phone=call.user.phone,
			answered=call.answered,
			hidden=call.hidden
		) for call in calls]
		return calls_schemas
	
	def get(self, db_session: Session, call_id: int):
		call = db_session.query(Call).options(lazyload('manager'), lazyload('user')).get(call_id)
		if call is None:
			raise NoResultFound('Call not found')
		return CallSchema(
			id=call.id,
			community_id=call.community_id,
			manager_phone=call.manager.phone,
			client_phone=call.user.phone if call.hidden == False else None,
			answered=call.answered,
			hidden=call.hidden,
		)

	def get_call_asterisk(self, db_session: Session, call_id: int):
		call_asterisk = db_session.query(Call).options(lazyload('manager'), lazyload('user'), lazyload('community')).get(call_id)
		if call_asterisk is None:
			raise NoResultFound('Call not found')
		return CallAsterisk(
			id=call_id,
			community_name=call_asterisk.community.name,
			manager_name=call_asterisk.manager.name,
			manager_phone=call_asterisk.manager.phone,
			user_name=f'{call_asterisk.user.first_name} {call_asterisk.user.last_name}',
			user_phone=call_asterisk.user.phone,
			call_time=call_asterisk.call_time
		)


call = CallService()
