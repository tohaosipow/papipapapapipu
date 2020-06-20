from pydantic import BaseModel


class SettingBase(BaseModel):
    welcome_speech: str = None
    color_button: str = None
    community_id: int = None


class SettingBaseInDB(SettingBase):
    id: int = None

    class Config:
        orm_mode = True


class SettingSet(SettingBase):
    welcome_speech: str
    color_button: str
    community_id: int


class Setting(SettingBaseInDB):
    pass


class SettingUpdate(BaseModel):
    welcome_speech: str
    color_button: str
