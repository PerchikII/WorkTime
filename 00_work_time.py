import time


import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.lang.builder import Builder
from kivy.properties import ListProperty,StringProperty

Builder.load_file("00_work_time.kv")

month_lst = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
             'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

time_now = time.time() # Секунды с начала эпохи
time_day = time.localtime(time_now) # Текущее число
CURRENT_DAY = time.strftime("%d", time_day)
number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]
CURRENT_HOURS = time.strftime("%H", time_day)
CURRENT_MINUTES = time.strftime("%M", time_day)

class Pages(Carousel):
    hours_spinner_str = StringProperty(CURRENT_HOURS)
    minutes_spinner_str = StringProperty(CURRENT_MINUTES)
    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)
    month_lst_property = ListProperty(month_lst)  # Устан.всех месяцев в Spinner
    label_month_lst_property = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        print(self.ids.keys())

    def create_date(self):
        self.label_month_lst_property.clear()
        day = self.ids['day'].text
        month = self.ids['month'].text
        self.label_month_lst_property.append(day)
        self.label_month_lst_property.append(month)



class MyApp(App):
    def build(self):
        return Pages()


if __name__ == '__main__':
    MyApp().run()
