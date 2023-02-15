from datetime import datetime, timedelta
from enum import Enum
from .activity import Activity

activities: list[Activity] = []
class TIME_COLLISION_TYPE(Enum):
    START = 1
    END = 2
    INSIDE = 3
    OUTSIDE = 4

def list_day_activities():
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    one_hour = timedelta(hours=1)
    day = []
    current_act = None
    selected_act = None
    valid_activities = list(filter(
        lambda act: act.start and act.end,
        activities
    ))
    for i in range(24):
        no_activity = Activity(
            today + timedelta(hours=i),
            today + timedelta(hours=i+1)
        )
        activity = list(filter(
            lambda act:
               act.start <= no_activity.start and
               act.end >= no_activity.end,
            valid_activities
        ))
        activity = activity if activity else None
        if activity and activity not in day:
            day.append(activity)
            current_act = activity
        elif activity and activity in day:
            # activity bigger than 1h
            pass
        elif current_act and no_activity.start > current_act.end:
            no_activity.end = current_act.end
            day.append(no_activity)
            current_act = no_activity
        else:
            day.append(no_activity)
            current_act = no_activity

        if current_act.start.hour == now.hour:
            selected_act = i

    return [day, selected_act]

def time_collision_detection(act: Activity, no_act: Activity):
    '''
    ca = current activity
    oa = other activity

    start collision:
         ca
    |---|   |----|
    |--| |------|
       oa <-
    ca.start > oa.start
    ca.start < oa.end
    '''
    if act.start >= no_act.start and act.start <= no_act.end:
        return TIME_COLLISION_TYPE.START
    '''
    end collision:
         ca
    |---|   |----|
    |------| |------|
        -> oa
    ca.end > oa.start
    ca.end < oa.end
    '''
    if act.end >= no_act.start and act.end <= no_act.end:
        return TIME_COLLISION_TYPE.END
    '''
    inside collision:
         ca
    |---|   |----|
    |----|X|------|
         oa
    ca.start < oa.start
    ca.end > oa.start
    ca.start < oa.end
    ca.end > oa.end
    '''
    if (
        act.start <= no_act.start and act.end >= no_act.start and
        act.start <= no_act.end and act.end >= no_act.end
    ):
        return TIME_COLLISION_TYPE.INSIDE
    '''
    outside collision:
         ca
    |---|   |----|
    |--|      |--|
        ⬇ oa ⬇
    |--|o|ca|o|--|
    ca.start > oa.start
    ca.end > oa.start
    ca.start < oa.end
    ca.end < oa.end
    '''
    if (
        act.start >= no_act.start and act.end >= no_act.start and
        act.start <= no_act.end and act.end <= no_act.end
    ):
        return TIME_COLLISION_TYPE.OUTSIDE
