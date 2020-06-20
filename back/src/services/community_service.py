from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models import Community, Manager, User
from schemas.community import CommunityCreate
from schemas.manager import ManagerCreate


class CommunityService():
    def create(self, db_session: Session, community_to_create: CommunityCreate):
        community = Community(
            community_vk_id=community_to_create.community_vk_id,
            avatar_url=community_to_create.avatar_url,
            name=community_to_create.name,
        )
        for manager in community_to_create.managers:
            manager = Manager(phone=manager.phone, name=manager.name, is_blocked=False)
            community.managers.append(manager)
            
        for admin in community_to_create.admins:
            user = db_session.query(User).get(admin)
            if user is not None:
                community.admins.append(user)
                
        db_session.add(community)
        db_session.commit()
        db_session.refresh(community)
        return community
    
    def get(self, db_session: Session, community_id: int):
        community = db_session.query(Community).options(lazyload('managers'), lazyload('admins')).get(community_id)
        if community is None:
            raise NoResultFound('Community not found')
        return community

    def get_by_vk_id(self, db_session: Session, community_vk_id: int):
        community = db_session.query(Community).options(lazyload('managers'), lazyload('admins'))\
            .filter_by(community_vk_id=community_vk_id)\
            .first()
        if community is None:
            raise NoResultFound('Community not found')
        return community

    def add_manager(self, db_session: Session, community_id: int, manager_to_add: ManagerCreate):
        community = db_session.query(Community).options(lazyload('managers')).get(community_id)
        manager = Manager(
            phone=manager_to_add.phone,
            name=manager_to_add.name,
            is_blocked=manager_to_add.is_blocked
        )

        community.managers.append(manager)
        db_session.add(community)
        db_session.commit()
        db_session.refresh(community)
        return community

    def remove_manager(self, db_session: Session, manager_id):
        manager = db_session.query(Manager).get(manager_id)
        if manager is None:
            raise NoResultFound('Manager not found')

        db_session.delete(manager)
        db_session.commit()
        return manager



community = CommunityService()
