from dataclasses import dataclass
from datetime import datetime, timedelta

NO_ACTIVITY = 'FREE'

@dataclass
class Activity:
    start: datetime = None
    end: datetime = None
    name: str = NO_ACTIVITY
    color: str = None
    notification: bool = None
    alarm: str|bool = None

    def __repr__(self):
        time = self.time()
        return f'{time} - {self.name}'

    def time_start(self):
        return self.start.strftime('%H:%M') if self.start else 'XX:XX'

    def time_end(self):
        return self.end.strftime('%H:%M') if self.end else 'XX:XX'

    def time(self):
        start = self.time_start()
        end = self.time_end()
        return f'{start} {end}'

    def is_free(self):
        return self.name == NO_ACTIVITY

    def detail(self, placeholder=False):
        notify = 'on' if self.notification else 'off'
        alarm = self.alarm if self.alarm else 'off'
        detail = f'''name: {self.name}
color: {self.color}
%time%notification: {notify}
alarm: {alarm}'''
        if not placeholder:
            detail = detail.replace('%time%', '')
        return detail

    def detail_full(self):
        start = self.time_start()
        end = self.time_end()
        return self.detail(True).replace('%time%', f'''start: {start}
end: {end}
                                         ''')

    def clone(self):
        return Activity(
            self.start, self.end,
            self.name, self.color,
            self.notification, self.alarm
        )

    def update(self, act):
        self.start = act.start
        self.end = act.end
        self.name = act.name
        self.color = act.color
        self.notification = act.notification
        self.alarm = act.alarm

def week_day(day=None):
    date = None
    if not day:
        date = datetime.now()
    else:
        date = datetime.min + timedelta(days=day)
    return date.strftime('%A')

def week_time():
    return datetime.now().strftime('%A - %H:%M')

def format_timedelta(time):
    time = str(time)
    if 'day' in time:
        time = time.split(', ')[1]
    return time[:-3]

# def format_timedelta(s):
    # s = s.dt.total_seconds()

    # seconds = (s%60).astype(int).astype(str).str.zfill(2)
    # minutes = (s//60%60).astype(int).astype(str).str.zfill(2)
    # hours = (s//3600).astype(int).astype(str)

    # return hours+':'+minutes+':'+seconds
