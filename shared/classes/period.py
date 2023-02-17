from dataclasses import dataclass
from datetime import datetime, timedelta
from peewee import CharField, DateTimeField, ForeignKeyField, BooleanField
from playhouse.hybrid import hybrid_property
from ..helpers import format_timedelta
from .activity import Activity
from .base import Base
from ..repository import db

class Period(Base):
    start = DateTimeField()
    end = DateTimeField()
    activity: Activity = ForeignKeyField(Activity, null=True)

    def __repr__(self):
        time = self.time()
        act = str(self.activity) if self.activity else ''
        return f'{time} {act}'

    def __str__(self):
        return self.__repr__()

    def date_to_current_week(self, date: datetime):
        now = datetime.now()
        # get this week start time
        monday = now - timedelta(days=now.weekday())
        monday = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # get time from the start of the date week until the current timestamp
        _, _, _, h, m, s, wd, *_ = date.timetuple()
        time_week = timedelta(wd, hours=h, minutes=m, seconds=s)
        # set timestamp in current week
        return monday + time_week

    @hybrid_property
    def start_current_week():
        return self.date_to_current_week(self.start)

    @hybrid_property
    def end_current_week():
        return self.date_to_current_week(self.end)

    def time_format(self, time: datetime):
        return time.strftime('%H:%M') if time else 'XX:XX'

    def format_times(self):
        return self.time_format(self.start), self.time_format(self.end)

    def time(self):
        start, end = self.format_times()
        return f'{start} {end}'

    def detail(self):
        start, end = self.format_times()
        return self.activity.detail() + f'\nstart: {start}\nend: {end}'

db.create_tables(Period)
