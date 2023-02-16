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

def select_time(lines, row):
    time = week_time()
    selected = fzf.prompt(
        lines,
        f'--reverse --sync --header "⏰ {time}" --bind start:pos:{row}'
    )
    return single_result(selected)

def select_activity(title, activities):
    selected = fzf.prompt(
        activities,
        f'--reverse --sync --header "🏋 {title}"'
    )
    return single_result(selected)

def edit_activity(act: Activity=None, warn: bool=False):
    if warn:
        info("There's no activities registered, you're being redirected to create a new activity")
    changed_act = act.clone() if act else Activity()

    if not changed_act.is_free():
        option = confirm(f'Do you want to change the name from {act.name}')
        if option:
            changed_act.name = input('name: ')
        option = confirm(f'Do you want to change the color from {act.name}')
        if option:
            changed_act.color = input('color: ')
    else:
        changed_act.name = input('name: ')
        changed_act.color = input('color: ')
    changed_act.notification = confirm('Do you want to notify when this activity is about to start?')
    changed_act.alarm = confirm('Do you want to set a alarm sound when this activity is about to start?')
    if changed_act.alarm:
        changed_act.alarm = select('Select alarm sound:', ['old', 'ring', 'android'])

    save = confirm('Do you want to save?', preview=changed_act.detail())
    if save:
        if act and not act.is_free():
            act.update(changed_act)
        return changed_act
    else:
        return None

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

def assign_activity(period: Period, act: Activity):
    changed_period = period.clone()
    changed_period.activity = act
    changed_period.start = select_datetime('START DAY', period.start)
    changed_period.end = select_datetime('END DAY', period.end)
    time = changed_period.time()
    
    save = confirm(f'Do you want to assign {act.name} to {time}?',
                   preview=changed_period.detail())
    # TODO: verify time conflicts
    if save:
        # period.update(changed_period) ???
        return changed_period
    else:
        return None

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
