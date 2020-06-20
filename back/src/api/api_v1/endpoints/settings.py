from starlette import status

import services

from api.utils.db import get_db
from database.session import Session
from fastapi import APIRouter, Depends, HTTPException

from schemas.settings import Setting, SettingUpdate

from schemas.settings import SettingSet

router = APIRouter()


@router.post('/setSetting', response_model=Setting)
def set_settings(
        setting_to_set: SettingSet,
        db: Session = Depends(get_db)
):
    if setting_to_set is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        setting = services.setting.set_settings(db, setting_to_set)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return setting


@router.put('/updateSetting/{community_id}', response_model=Setting)
def update_settings(
        community_id: int,
        setting_to_update: SettingUpdate,
        db: Session = Depends(get_db)
):
    if setting_to_update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        setting = services.setting.update_settings(db, community_id, setting_to_update)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return setting


@router.get('/getSettingByCommunityId/{community_id}', response_model=Setting)
def get_setting_by_community_id(
        community_id: int,
        db: Session = Depends(get_db)
):
    try:
        settings = services.setting.get_settings(db, community_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return settings
