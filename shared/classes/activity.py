from dataclasses import dataclass
from peewee import CharField, BooleanField
from .base import Base
from ..repository import db

NO_ACTIVITY = 'FREE'

class Activity(Base):
    name = CharField(default=NO_ACTIVITY)
    color = CharField(default='white')
    notification = BooleanField()
    alarm = CharField()

    def __repr__(self):
        return f'{self.name} [{self.color}]'

    def __str__(self):
        return self.__repr__()

    def is_free(self):
        return self.name == NO_ACTIVITY

    def detail(self):
        notify = 'on' if self.notification else 'off'
        alarm = self.alarm if self.alarm else 'off'
        detail = f'''name: {self.name}\n\
            color: {self.color}\n\
            notification: {notify}\n\
            alarm: {alarm}'''
        return detail

    def detail_full(self):
        detail = self.detail()
        return detail

db.create_tables(Activity)
