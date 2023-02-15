from datetime import timedelta

class Event:
    name = StringProperty()
    color = StringProperty()
    start = timedelta()
    end = timedelta()
    notification = BooleanProperty()
    read_event_name = BooleanProperty()
    alarm_sound =  StringProperty()

    # def __init__():

