from datetime import datetime
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
# print('Name', __name__)
from .components.event_card.event_card import EventCard
from kivymd.uix.pickers import MDTimePicker
# import kivymd.icon_definitions as icons

class MainApp(MDApp):
    def build(self):
        self.count = 0;
        self.time = None;
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Purple'
        return Builder.load_file('mobile/src/app.kv')

    # def on_start(self):
        # for i in range(20):
            # self.root.ids.box.add_widget(
                # EventCard(
                    # line_color=(0.2, 0.2, 0.2, 0.8),
                    # style="filled",
                    # text=f'Hello #{i}',
                    # md_bg_color="#f4dedc",
                    # shadow_offset=(0, -1),
                # )
            # )
    
    def add_event(self):
        # print('Time to add event!')
        # self.count += 1;
        # self.root.ids.title.text = f'Counting: {self.count}'

        time_dialog = MDTimePicker()
        # previous_time = datetime.strptime("13:20:00", '%H:%M:%S').time()
        previous_time = datetime.now()

        time_dialog.bind(on_save=self.get_time)
        time_dialog.set_time(previous_time)
        time_dialog.open()
        print('hello time!')
        print('time:', time_dialog.time)

    def get_time(self, instance, time):
        print('time:', time, type(time))
        # Clock.schedule_lifecycle_aware_del_safe(self, self.alarm, self.seila)
        # from datetime import timedelta 
        # time = datetime.strptime(time, '%H:%M:%S').time()
        self.time = time
        time = datetime.now().replace(hour=time.hour, minute=time.minute, second=0)
        seconds =  time - datetime.now()
        print('time date', time)
        print('seconds', seconds.total_seconds())
        Clock.schedule_once(self.alarm, seconds.total_seconds())


    def alarm(self, time):
        print('ALARM!', self.time)
        self.root.ids.title.text = f'ALARM of {self.time}'

if __name__ == 'weekplanner.mobile.src.app':
    app = MainApp()
    app.run()
