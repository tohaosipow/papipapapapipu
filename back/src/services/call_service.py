from datetime import datetime, timezone

from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models import Call, Community, Manager, User
from schemas.call import CallCreate, CallAsterisk
from schemas.call import Call as CallSchema


class CallService:
    def create(
        self,
        db_session: Session,
        call_to_create: CallCreate,
        community_id: int,
        user_id: int,
    ):
        community = (
            db_session.query(Community).options(lazyload("managers")).get(community_id)
        )
        if community is None:
            raise NoResultFound("Community not found")

        if len(community.managers) == 0:
            raise NoResultFound("Managers not found")

        manager = community.managers[0]
        user = db_session.query(User).get(user_id)
        if user is None:
            raise NoResultFound("User not found")

        call = Call(
            community_id=community_id,
            client_phone=call_to_create.client_phone,
            hidden=call_to_create.hidden,
            answered=False,
            manager_id=manager.id,
            user_id=user_id,
            call_time=datetime.utcnow() if call_to_create.call_time is None else call_to_create.call_time.astimezone(timezone.utc),
        )

        db_session.add(call)
        db_session.commit()
        db_session.refresh(call)

        return CallSchema(
            id=call.id,
            community_id=call.community_id,
            manager_name=call.manager.name,
            manager_phone=call.manager.phone,
            client_name=f"{call.user.first_name} {call.user.last_name}",
            client_phone=call.user.phone if call.hidden == False else None,
            client_avatar=call.user.avatar_url,
            answered=call.answered,
            hidden=call.hidden,
            call_time=call.call_time,
        )

    def get_call_history(self, db_session: Session, community_id: int):
        community = db_session.query(Community).get(community_id)
        if community is None:
            raise NoResultFound("Community not found")

        calls = (
            db_session.query(Call)
            .options(lazyload("manager"), lazyload("user"))
            .filter_by(community_id=community_id)
            .all()
        )
        calls_schemas = [
            CallSchema(
                id=call.id,
                community_id=call.community_id,
                manager_name=call.manager.name,
                manager_phone=call.manager.phone,
                client_name=f"{call.user.first_name} {call.user.last_name}",
                client_phone=call.user.phone if call.hidden == False else None,
                client_avatar=call.user.avatar_url,
                answered=call.answered,
                hidden=call.hidden,
                call_time=call.call_time,
            )
            for call in calls
            if call.manager is not None
        ]
        return calls_schemas

    def get(self, db_session: Session, call_id: int):
        call = (
            db_session.query(Call)
            .options(lazyload("manager"), lazyload("user"))
            .get(call_id)
        )
        if call is None:
            raise NoResultFound("Call not found")
        if call.manager is None:
            return None
        return CallSchema(
            id=call.id,
            community_id=call.community_id,
            manager_name=call.manager.name,
            manager_phone=call.manager.phone,
            client_name=f"{call.user.first_name} {call.user.last_name}",
            client_phone=call.user.phone if call.hidden == False else None,
            client_avatar=call.user.avatar_url,
            answered=call.answered,
            hidden=call.hidden,
            call_time=call.call_time,
        )

    def get_call_asterisk(self, db_session: Session, call_id: int):
        call_asterisk = (
            db_session.query(Call)
            .options(lazyload("manager"), lazyload("user"), lazyload("community"))
            .get(call_id)
        )
        if call_asterisk is None:
            raise NoResultFound("Call not found")
        return CallAsterisk(
            id=call_id,
            community_name=call_asterisk.community.name,
            manager_name=call_asterisk.manager.name,
            manager_phone=call_asterisk.manager.phone,
            user_name=f"{call_asterisk.user.first_name} {call_asterisk.user.last_name}",
            user_phone=call_asterisk.client_phone or call_asterisk.user.phone,
            call_time=call_asterisk.call_time,
        )

    def remove(self, db_session: Session, call_id: int):
        call = db_session.query(Call).get(call_id)
        if call is None:
            raise NoResultFound("Call not found")
        db_session.delete(call)
        db_session.commit()
        return call


call = CallService()
