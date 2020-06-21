from sqlalchemy.orm import lazyload
from sqlalchemy.orm.exc import NoResultFound

import services
from database.session import Session
from models import Community, Manager, User
from schemas.community import CommunityCreate
from schemas.manager import ManagerCreate


class CommunityService:
    def create(
        self, db_session: Session, community_to_create: CommunityCreate, user_id: int
    ):
        info = services.vk_service.get_community_info(
            community_to_create.api_key, community_to_create.community_vk_id
        )
        community = Community(
            community_vk_id=community_to_create.community_vk_id,
            avatar_url=info["photo_200"],
            name=info["name"],
        )

        user = db_session.query(User).get(user_id)
        if user is not None:
            community.admins.append(user)

        db_session.add(community)
        db_session.commit()
        db_session.refresh(community)
        return community

    def remove(self, db_session: Session, community_id: int, user_id: int):
        community = (
            db_session.query(Community).options(lazyload("admins")).get(community_id)
        )
        if community is None:
            raise NoResultFound("Community not found")

        user = db_session.query(User).get(user_id)
        if user is None:
            raise NoResultFound("User not found")

        if user not in community.admins:
            raise Exception("User is not admin of this community")

        db_session.delete(community)
        db_session.commit()
        return community

    def get(self, db_session: Session, community_id: int):
        community = (
            db_session.query(Community)
            .options(lazyload("managers"), lazyload("admins"))
            .get(community_id)
        )
        if community is None:
            raise NoResultFound("Community not found")
        return community

    def get_by_vk_id(self, db_session: Session, community_vk_id: int):
        community = (
            db_session.query(Community)
            .options(lazyload("managers"), lazyload("admins"))
            .filter_by(community_vk_id=community_vk_id)
            .first()
        )
        if community is None:
            raise NoResultFound("Community not found")
        return community

    def add_manager(
        self, db_session: Session, community_id: int, manager_to_add: ManagerCreate
    ):
        community = (
            db_session.query(Community).options(lazyload("managers")).get(community_id)
        )
        manager = Manager(
            phone=manager_to_add.phone,
            name=manager_to_add.name,
            is_blocked=manager_to_add.is_blocked,
        )

        community.managers.append(manager)
        db_session.add(community)
        db_session.commit()
        db_session.refresh(community)
        return community

    def is_current_user_admin(
        self, db_session: Session, user_id: int, community_id: int
    ):
        community = (
            db_session.query(Community).options(lazyload("admins")).get(community_id)
        )
        if community is None:
            raise NoResultFound("Community not found")

        user = db_session.query(User).get(user_id)
        if user is None:
            raise NoResultFound("User not found")

        if user not in community.admins and not user.is_admin:
            return False

        return True

    def remove_manager(self, db_session: Session, manager_id):
        manager = db_session.query(Manager).get(manager_id)
        if manager is None:
            raise NoResultFound("Manager not found")

        db_session.delete(manager)
        db_session.commit()
        return manager


community = CommunityService()
