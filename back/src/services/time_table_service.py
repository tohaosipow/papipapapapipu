from sqlalchemy.orm.exc import NoResultFound

from database.session import Session
from models import TimeTable
from schemas.time_table import TimeTableSet, TimeTableUpdate


class TimeTableService:
    def add_time_table(self, db_session: Session, time_to_set: TimeTableSet):
        new_time_table = TimeTable(
            manager_id=time_to_set.manager_id,
            day_of_the_week=time_to_set.day_of_the_week,
            start_work=time_to_set.start_work,
            end_work=time_to_set.end_work
        )

        db_session.add(new_time_table)
        db_session.commit()
        db_session.refresh(new_time_table)
        return new_time_table

    def get_time_table(self, db_session: Session, manager_id: int, day: str) -> TimeTable:
        time_table = db_session.query(TimeTable).filter_by(manager_id=manager_id)\
                                                .filter_by(day_of_the_week=day)\
                                                .order_by(TimeTable.start_work)\
                                                .all()
        return time_table

    def update_time_table(self, db_session: Session, time_table_id: int, time_to_update: TimeTableUpdate):
        update_time = db_session.query(TimeTable).filter_by(id=time_table_id).first()
        if update_time is None:
            raise NoResultFound('Time Table not found')

        update_time.day_of_the_week = time_to_update.day_of_the_week
        update_time.start_work = time_to_update.start_work
        update_time.end_work = time_to_update.end_work

        db_session.add(update_time)
        db_session.commit()
        db_session.refresh(update_time)
        return update_time

    def remove_time_table(self, db_session: Session, time_table_id: int):
        time_table = db_session.query(TimeTable).get(time_table_id)
        if time_table_id is None:
            raise NoResultFound('Time Table not found')

        db_session.delete(time_table)
        db_session.commit()
        return time_table


time_table = TimeTableService()
