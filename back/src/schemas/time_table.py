from datetime import time

from pydantic.main import BaseModel


class TimeTableBase(BaseModel):
    manager_id: int
    day_of_the_week: str
    start_work: time
    end_work: time


class TimeTableBaseInDB(TimeTableBase):
    id: int = None

    class Config:
        orm_mode = True


class TimeTableSet(TimeTableBase):
    pass


class TimeTable(TimeTableBaseInDB):
    pass


class TimeTableUpdate(BaseModel):
    day_of_the_week: str
    start_work: time
    end_work: time
