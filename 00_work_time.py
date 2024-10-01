import time


import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.carousel import Carousel
from kivy.lang.builder import Builder
from kivy.properties import ListProperty,StringProperty

import os
"""Установить kv файл в директорию совместно в main.py"""
dirname = os.path.split(os.path.abspath(__file__))
Builder.load_file(os.path.join(dirname[0],"00_work_time.kv"))
print(os.path.join(dirname[0]))

month_lst = ['Январь', 'Февраля', 'Марта', 'Апреля','Мая', 'Июня',
             'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

time_now = time.time() # Секунды с начала эпохи
time_day = time.localtime(time_now) # Текущее число
CURRENT_DAY = time.strftime("%d", time_day)
number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]
CURRENT_HOURS = time.strftime("%H", time_day)
CURRENT_MINUTES = time.strftime("%M", time_day)

class Pages(Carousel):
    hours_start_work = StringProperty("HStW")
    minutes_start_work_minutes = StringProperty("00")

    hours_end_work = StringProperty("HEndW")
    hours_start_lunch = StringProperty("HStlanch")
    hours_end_lanch = StringProperty("HEndLanch")

    minutes_spinner_str = StringProperty("00")
    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)
    month_lst_property = ListProperty(month_lst)  # Устан.всех месяцев в Spinner
    label_month_lst_property = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        # self._day = self.day_spinner_str
        # self._month = self.month_spinner_str
        self._hours_start_work = self.hours_start_work
        self._minutes = self.minutes_start_work_minutes

    def create_start_work_time(self,spinner):
        print(spinner.uid)
        if spinner.uid == 118:
            self.hours_start_work = spinner.text
        elif spinner.uid == 159:
            self.minutes_start_work_minutes = spinner.text
        print(self.hours_start_work)
        print(self.minutes_start_work_minutes)



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
