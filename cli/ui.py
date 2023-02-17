from subprocess import Popen, PIPE
from pyfzf.pyfzf import FzfPrompt
from datetime import datetime
from ..shared.classes.activity import Activity
from ..shared.classes.period import Period
from ..shared.helpers import week_time, week_day

fzf = FzfPrompt()

def single_result(selected):
    if not selected:
        return None
    return selected[0]

def list_today(lines, row):
    time = week_time()
    selected = fzf.prompt(
        lines,
        f'--reverse --sync --header "⏰ {time}" --bind start:pos:{row}'
    )
    return single_result(selected)

def select_activity(title, activities):
    activities.append('NEW Activity')
    activities.append('CHANGE Time period')
    activities.append('FREE Time period')
    selected = fzf.prompt(
        activities,
        f'--reverse --sync --header "🏋 {title}"'
    )
    return single_result(selected)

def edit_activity(act: Activity=None, warn: bool=False):
    if warn:
        info("There's no activities registered, you're being redirected to create a new activity")
    if not act:
        act = Activity()
    if not act.is_free():
        option = confirm(f'Do you want to change the name from {act.name}')
        if option:
            act.name = input('name: ')
        option = confirm(f'Do you want to change the color from {act.name}')
        if option:
            act.color = input('color: ')
    else:
        act.name = input('name: ')
        act.color = input('color: ')
    act.notification = confirm('Do you want to notify when this activity is about to start?')
    act.alarm = confirm('Do you want to set a alarm sound when this activity is about to start?')
    if act.alarm:
        act.alarm = select('Select alarm sound:', ['old', 'ring', 'android'])
    return act if confirm('Do you want to save?', preview=act.detail()) else False

def select_datetime(title: str, date: datetime):
    hour = str(date.hour).rjust(2, '0')
    fifteen_minutes = lambda i: str(i * 15).rjust(2, '0')
    minutes=list(map(
        lambda i: f'{hour}:{fifteen_minutes(i)}',
        range(4)
    ))
    minute = select(f'{title} - minute:', minutes)
    hour = int(hour)
    minute = int(minute.split(':')[1])
    return date.replace(hour=hour,minute=minute, second=0, microsecond=0)

def assign_activity(period: Period):
    period.start = select_datetime('START DAY', period.start)
    period.end = select_datetime('END DAY', period.end)
    time = period.time()
    
    # TODO: verify time conflicts
    return confirm(f'Do you want to assign {period.activity.name} to {time}?',
                   preview=period.detail())

def select(header, options):
    response = fzf.prompt(options, f'--header "{header}"')
    return single_result(response)

def confirm(question: str, as_bool: bool = True, preview=None):
    prev = ''
    if preview:
        prev = f'--preview "printf \'{preview}\'"'
    response = fzf.prompt(['Yes', 'No'], f'--header "🤔 {question}" {prev}')
    response = single_result(response)
    if not response and as_bool:
        return False
    elif response and as_bool:
        return response == 'Yes'
    return response

def info(say):
    return fzf.prompt(['Ok'], f'--header "ℹ {say}"')
