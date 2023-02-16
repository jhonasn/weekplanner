from datetime import datetime, timedelta

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
    if type(time) is datetime:
        return time.strftime('%H:%M')
    time = str(time)
    if 'day' in time:
        time = time.split(', ')[1]
    return time[:-3]
