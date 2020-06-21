from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

import services
from api.utils.db import get_db
from database.session import Session
from schemas.time_table import TimeTable, TimeTableSet, TimeTableUpdate

router = APIRouter()


@router.post("/addTimeTable", response_model=TimeTable)
def add_time_table(time_to_set: TimeTableSet, db: Session = Depends(get_db)):
    if time_to_set is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        table_table = services.time_table.add_time_table(db, time_to_set)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return table_table


@router.get(
    "/getTimeTableByManagerId/{manager_id}/dayOfTheWeek{day}",
    response_model=List[TimeTable],
)
def get_time_table_by_manager_id(
    manager_id: int, day: str, db: Session = Depends(get_db)
):
    try:
        time_table = services.time_table.get_time_table(db, manager_id, day)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return time_table


@router.put("/updateTimeTable/{manager_id}", response_model=TimeTable)
def update_settings(
    time_table_id: int, time_to_update: TimeTableUpdate, db: Session = Depends(get_db)
):
    if time_to_update is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        time_table = services.time_table.update_time_table(
            db, time_table_id, time_to_update
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return time_table


@router.delete("/removeTimeTable/{time_table_id}", response_model=TimeTable)
def remove_time_table(
    time_table_id: int, db: Session = Depends(get_db),
):
    try:
        time_table = services.time_table.remove_time_table(db, time_table_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return time_table
