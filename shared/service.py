from datetime import datetime, timedelta
from enum import Enum
from .classes.activity import Activity
from .classes.period import Period
from .repository import todayActivities

class TIME_COLLISION_TYPE(Enum):
    START = 1
    END = 2
    INSIDE = 3
    OUTSIDE = 4

def list_day_activities():
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    one_hour = timedelta(hours=1)
    day: list[Period] = []
    current_period = None
    selected_period = None
    valid_activities = list(filter(
        lambda term: term.start and term.end and not term.activity.is_free(),
        todayActivities
    ))
    for i in range(24):
        free_time = Period(
            today + timedelta(hours=i),
            today + timedelta(hours=i+1)
        )
        # time_collisions = list(filter(
            # lambda period: [time_collision_detection(period, free_time), period],
            # valid_activities
        # ))
        period = list(filter(
            lambda period:
               period.start <= free_time.start and
               period.end >= free_time.end,
            valid_activities
        ))
        period = period[0] if period else None
        if period and period not in day:
            day.append(period)
            current_period = period
        elif period and period in day:
            # activity bigger than 1h
            pass
        elif current_period and free_time.start > current_period.end:
            free_time.end = current_period.end
            day.append(free_time)
            current_period = free_time
        else:
            day.append(free_time)
            current_period = free_time

        if current_period.start.hour == now.hour:
            selected_period = i

    return [day, selected_period]

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

    return None
