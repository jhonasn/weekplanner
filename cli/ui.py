from subprocess import Popen, PIPE
from pyfzf.pyfzf import FzfPrompt
from datetime import datetime
from ..shared.activity import Activity, week_time, week_day
from ..shared.repository import activities

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

def select_activity(title):
    selected = fzf.prompt(
        activities,
        f'--reverse --sync --header "🏋 {title}"'
    )
    return single_result(selected)

def edit_activity(act: Activity=None, warn: bool=False):
    if warn:
        info("There's no activities registered, you're being redirected to create a new activity")
    changed_act = act.clone() if act else Activity()

    cmd_header('New Activity:')

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

    # cmd_header('The new activity:')
    # print(changed_act.detail())
    # print()

    save = confirm('Do you want to save?', preview=changed_act.detail())
    if save:
        if act and not act.is_free():
            act.update(changed_act)
        return changed_act
    else:
        return None

def select_datetime(title: str, date: datetime):
    # week_days = list(map(lambda i: week_day(i), range(7)))
    # day = select(f'{title} - day of the week:', week_days)
    # day = week_days.index(day)
    # hour = select(f'{title} - hour:', range(24))
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

def assign_activity(act: Activity):
    changed_act = act.clone()
    changed_act.start = select_datetime('START DAY', act.start)
    changed_act.end = select_datetime('END DAY', act.end)
    time = changed_act.time()
    
    save = confirm(f'Do you want to assign {act.name} to {time}?',
                   preview=changed_act.detail_full())
    # TODO: verify time conflicts
    # already_on_activities = list(filter(
        # lambda a: a.name == act.name and a.start and a.end,
        # activities
    # ))
    if save:
        # if already_on_activities:
            # activities.append(changed_act)
        # else:
            # act.update(changed_act)
        activities.append(changed_act)
    return changed_act

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

def cmd_header(title):
    print('--------------------------------------')
    print(title)
    print('--------------------------------------')
    print()

# process = Popen(command, stdout=PIPE, stderr=PIPE)
# stdout, stderr = process.communicate()
# print(stdout, stderr)
# Popen(f"bash -c 'fzf --preselect=\\'{selected}\\' <<< \"{lines}\"'", shell=True)
    # bash -c "fzf --preselect='{selected}' <<< '{lines}'"
# with open('./temp', 'w') as f:
    # f.write(lines)
# cmd = f"cat ./temp | fzf --sync --bind start:pos:{row}"
# print(cmd)
# Popen(cmd, shell=True)
