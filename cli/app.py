from ..shared.classes.activity import Activity
from ..shared.classes.period import Period
from ..shared.service import list_day_activities
from .ui import list_today, edit_activity, assign_activity, info, confirm, select_activity

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
    selected = list_today(buffer, start_row + 4)
    if selected:
        if 'exit' in selected:
            return
        index = buffer.index(selected)
        if open_crud_menu(selected) == False:
            period = day[index - 3]
            activity_assignment(period)
            # print('i:', index, 's:', selected, 'a:', period)
        init()

def open_crud_menu(selected, period: Period = None):
    change_options = ['DELETE', 'FREE']
    edit_options = ['NEW', 'CHANGE']
    if not selected:
        return None
    elif 'Activity' in selected:
        option = selected.split(' ')[0]
        if 'DELETE' in selected:
            delete_activity()
            return None
        elif selected in edit_options:
            return change_activity(option)
        else:
            print('INVALID OPTION 🤔')
    elif 'Time period' in selected:
        if 'CHANGE' in selected:
            if assign_activity(period):
                period.save()
        else:
            period.delete_instance()
        return None
    else:
        return False

def change_activity(action):
    if action == 'NEW':
        act = edit_activity()
        if act:
            act.save()
            return act
    elif not Activity.count():
        info('No activities registered')
        return None
    else:
        act = activity_selection('CHANGE Activity')
        if act:
            if edit_activity(act):
                act.save()
                return act


def delete_activity():
    activities = Activity.list()
    if not activities:
        info('No activities registered')
    else:
        act: Activity = activity_selection('DELETE Activity')
        response = confirm(f'Are you sure you want to delete the activity {act.name}?')
        if response:
            act.delete_instance(True)

def activity_selection(title, period: Period):
    activities = Activity.list()
    buffer = [str(act) for act in activities]
    selected = select_activity(title, activities)
    act = open_crud_menu(selected, period)
    if act:
        return act
    elif act == False:
        index = buffer.index(selected)
        return activities[index]

def activity_assignment(period: Period):
    time = period.time()
    is_new_activity = period.activity.is_free() and not Activity.count()
    if is_new_activity:
        if edit_activity(period.activity, True):
            period.activity.save()
    else:
        period.activity = activity_selection(f'SELECT one activity to {time}', period)
    if period and period.activity and assign_activity(period):
        period.save()

if __name__ == 'weekplanner.cli.app':
    init()
