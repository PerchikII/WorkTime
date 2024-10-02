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
    """Читай переменные. Их имена обо всём говорят."""
    hours_start_work = StringProperty("00")
    minutes_start_work = StringProperty("00")

    hours_end_work = StringProperty("00")
    minutes_end_work = StringProperty("00")

    hours_start_lunch = StringProperty("00")
    minutes_start_lunch = StringProperty("00")


    hours_end_lunch = StringProperty("HEndLanch")
    minutes_end_lunch = StringProperty("MinStlanch")

    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)

    month_lst_property = ListProperty(month_lst)  # Устан.всех месяцев в Spinner
    label_month_lst_property = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label



    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        # self._hours_start_work = self.hours_start_work
        # self._minutes_start_work = self.minutes_start_work
        #
        # self._hours_end_work = self.hours_end_work
        # self._minutes_end_work = self.minutes_end_work
        #
        # self._hours_start_lunch = self.hours_start_lunch
        # self._minutes_start_lunch = self.minutes_start_lunch
        #
        # self._hours_end_lunch = self.hours_end_lanch
        # self._minutes_end_lunch = self.minutes_end_lunch







    def create_start_work_time(self,spinner):
        match spinner.uid:
            case  116:
                self.hours_start_work = spinner.text
                print(spinner.uid,self.hours_start_work)
            case  157:
                self.minutes_start_work = spinner.text
                print(spinner.uid, self.minutes_start_work)
            case  290:
                self.hours_end_work = spinner.text
                print(spinner.uid, self.hours_end_work)
            case  331:
                self.minutes_end_work = spinner.text
                print(spinner.uid, self.minutes_end_work)
            case  204:
                self.hours_start_lunch = spinner.text
                print(spinner.uid, self.hours_start_lunch)
            case  245:
                self.minutes_start_lunch = spinner.text
                print(spinner.uid, self.minutes_start_lunch)
            case  378:
                self.hours_end_lunch = spinner.text
                print(spinner.uid, self.hours_end_lunch)
            case  419:
                self.minutes_end_lunch = spinner.text
                print(spinner.uid, self.minutes_end_lunch)








    def create_date(self):
        self.label_month_lst_property.clear()
        day = self.ids['day'].text
        month = self.ids['month'].text
        self.label_month_lst_property.append(day)
        self.label_month_lst_property.append(month)




class MyApp(App):
    def build(self):
        return Pages()
    def quit_program(self):
        exit()

if __name__ == '__main__':
    MyApp().run()
