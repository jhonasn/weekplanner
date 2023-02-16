from ..shared.classes.activity import Activity
from ..shared.classes.period import Period
from ..shared.service import list_day_activities, add, count, query
from .ui import select_time, edit_activity, assign_activity, info, confirm, select_activity

def init():
    day, selected_act = list_day_activities()
    show_day(day, selected_act)

def show_day(day, start_row):
    buffer: list[str] = []
    buffer.append('NEW Activity')
    buffer.append('CHANGE Activity')
    buffer.append('DELETE Activity')
    buffer += [str(period) for period in day]
    buffer.append('QUIT exit')
    selected = select_time(buffer, start_row + 4)
    if selected:
        if 'exit' in selected:
            return
        index = buffer.index(selected)
        change_options = ['NEW', 'CHANGE', 'DELETE']
        if 'Activity' in selected:
            option = selected.split(' ')[0]
            if 'DELETE' in selected:
                delete_activity()
            elif option in change_options:
                change_activity(option)
            else:
                print('INVALID OPTION 🤔')
        else:
            period = day[index - 3]
            activity_assignment(period)
            # print('i:', index, 's:', selected, 'a:', period)
        init()

def change_activity(action):
    if action == 'NEW':
        act = edit_activity()
        if act:
            add(act)
    elif not count(act):
        info('No activities registered')
    else:
        act = activity_selection('CHANGE Activity')
        if act:
            edit_activity(act)

def delete_activity():
    if not activities:
        info('No activities registered')
    else:
        act = activity_selection('DELETE Activity')
        response = confirm(f'Are you sure you want to delete the activity {act.name}?')
        if response:
            remove(act)

def activity_selection(title):
    activities = query(act)
    buffer = [str(act) for act in activities]
    selected = select_activity(title, activities)# put buffer on this?
    index = buffer.index(selected)
    return activities[index]

def activity_assignment(period: Period):
    time = period.time()
    is_new_activity = period.activity.is_free() and not count(Activity())
    if is_new_activity:
        selected_act = edit_activity(period.activity, True)
        if selected_act:
            add(selected_act)
    else:
        selected_act = activity_selection(f'SELECT one activity to {time}')
    period = assign_activity(period, selected_act)
    if period:
        add(period)

if __name__ == 'weekplanner.cli.app':
    init()
