from dataclasses import dataclass
# from .period import Period

NO_ACTIVITY = 'FREE'

@dataclass
class Activity:
    name: str = NO_ACTIVITY
    color: str = 'white'
    notification: bool = None
    alarm: str|bool = None
    id: int = None
    # occurences: list[Period] = []

    def __repr__(self):
        return f'{self.name} [{self.color}]'
        # return f'{self.name} [{self.color}] - {len(self.occurences)} times a week'

    def is_free(self):
        return self.name == NO_ACTIVITY

    def detail(self):
        notify = 'on' if self.notification else 'off'
        alarm = self.alarm if self.alarm else 'off'
        detail = f'''name: {self.name}\n\
            color: {self.color}\n\
            notification: {notify}\n\
            alarm: {alarm}'''
        return detail

    def detail_full(self):
        detail = self.detail()
        # detail += 'occurences:\n'
        # occurences = [str(oc) for oc in self.occurences]
        # occurences = '\n'.join(occurences)
        # return detail + occurences
        return detail

    def clone(self):
        return Activity(
            self.name, self.color,
            self.notification, self.alarm
        )

    def update(self, act):
        self.name = act.name
        self.color = act.color
        self.notification = act.notification
        self.alarm = act.alarm

