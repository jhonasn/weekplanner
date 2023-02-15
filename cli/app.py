from ..shared.activity import Activity
from ..shared.repository import activities, list_day_activities
from .ui import select_time, edit_activity, assign_activity, info, confirm, select_activity

def init():
    day, selected_act = list_day_activities()
    show_day(day, selected_act)

def show_day(day: list[Activity], start_row):
    buffer: list[str] = []
    buffer.append('NEW Activity')
    buffer.append('CHANGE Activity')
    buffer.append('DELETE Activity')
    buffer += [str(act) for act in day]
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
            act = day[index - 3]
            activity_assignment(act)
            # print('i:', index, 's:', selected, 'a:', act)
        init()

def change_activity(action):
    if action == 'NEW':
        print('yes new')
        act = edit_activity()
        if act:
            activities.append(act)
    elif not activities:
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
            activities.remove(act)

def activity_selection(title):
    buffer = [str(act) for act in activities]
    selected = select_activity(title)# put buffer on this?
    index = buffer.index(selected)
    return activities[index]

def activity_assignment(act: Activity):
    time = act.time()
    # import pdb;pdb.set_trace()
    if act.is_free() and not activities:
        act = edit_activity(act, True)
    # selected_act = activity_selection(f'SELECT one activity to {time}')
    # selected_act.start = act.start
    # selected_act.end = act.end
    assign_activity(act)

if __name__ == 'weekplanner.cli.app':
    init()
