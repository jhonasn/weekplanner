from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.lang import Builder

class EventCard(MDCard):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(EventCard, self).__init__(**kwargs)
        self.count = 0

    def change_card(self):
        self.count += 1
        self.ids.label.text = f'{self.text} {self.count}'

        print('Change card: ', self.text)

Builder.load_file('semanapp/components/event_card/event_card.kv')
