from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models.settings import Setting
from schemas.community import Community

from schemas.settings import SettingSet, SettingUpdate


class SettingService:
    def set_settings(self, db_session: Session, setting_to_set: SettingSet):
        new_setting = Setting(
            welcome_speech=setting_to_set.welcome_speech,
            color_button=setting_to_set.color_button,
            community_id=setting_to_set.community_id
        )

        db_session.add(new_setting)
        db_session.commit()
        db_session.refresh(new_setting)
        return new_setting

    def get_settings(self, db_session: Session, community_id: int) -> Setting:
        settings = db_session.query(Setting).filter_by(community_id=community_id).first()
        return settings

    def update_settings(self, db_session: Session, community_id: int, setting_to_update: SettingUpdate):
        update_setting = db_session.query(Setting).filter_by(community_id=community_id).first()
        if update_setting is None:
            raise NoResultFound('Setting not found')

        update_setting.welcome_speech = setting_to_update.welcome_speech
        update_setting.color_button = setting_to_update.color_button

        db_session.add(update_setting)
        db_session.commit()
        db_session.refresh(update_setting)
        return update_setting


setting = SettingService()
