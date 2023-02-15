from dataclasses import dataclass
from datetime import datetime
from .activity import Activity

@dataclass
class Period:
    start: datetime = None
    end: datetime = None
    activity: Activity = None

    def __post_init__(self):
        self.activity = Activity()

    def __repr__(self):
        time = self.time()
        act = str(self.activity) if self.activity else ''
        return f'{time} {act}'

    def time_start(self):
        return self.start.strftime('%H:%M') if self.start else 'XX:XX'

    def time_end(self):
        return self.end.strftime('%H:%M') if self.end else 'XX:XX'

    def time(self):
        start = self.time_start()
        end = self.time_end()
        return f'{start} {end}'

    def clone(self):
        return Period(self.start, self.end, self.activity)

    def update(self, period):
        self.start = period.start
        self.end = period.end
        self.activity = period.activity

    def detail(self):
        start = self.time_start()
        end = self.time_end()
        return self.activity.detail() + f'\nstart: {start}\nend: {end}'

