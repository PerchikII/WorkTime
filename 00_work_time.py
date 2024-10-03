import time
import os
from datetime import timedelta
import pickle


import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.properties import ListProperty,StringProperty,ObjectProperty


"""Установить kv файл в директорию совместно в main.py"""
dirname = os.path.split(os.path.abspath(__file__))
Builder.load_file(os.path.join(dirname[0],"00_work_time.kv"))

month_lst = ['Январь', 'Февраля', 'Марта', 'Апреля','Мая', 'Июня',
             'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

time_now = time.time() # Секунды с начала эпохи
time_day = time.localtime(time_now) # Текущее число

if time.strftime("%d", time_day)[0] == "0":
    CURRENT_DAY = time.strftime("%d", time_day)[1]

number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]
CURRENT_HOURS = time.strftime("%H", time_day)
CURRENT_MINUTES = time.strftime("%M", time_day)

# if not os.path.isfile("data_base.dat"):  # создание на HDD файла, если нету
        #     with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass

class Pages(Carousel):
    """Читай переменные. Их имена обо всём говорят."""

    hours_start_work = StringProperty("00")
    minutes_start_work = StringProperty("00")


    hours_end_work = StringProperty("00")
    minutes_end_work = StringProperty("00")

    hours_start_lunch = StringProperty("00")
    minutes_start_lunch = StringProperty("00")

    hours_end_lunch = StringProperty("00")
    minutes_end_lunch = StringProperty("00")

    total_hours_work = StringProperty("00")
    total_minutes_work = StringProperty("00")

    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)

    month_lst_property = ListProperty(month_lst)  # Устан.всех месяцев в Spinner
    label_month_lst_property = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label

    label_statistic = ObjectProperty()
    key_dict_total_data = CURRENT_DAY + " " + CURRENT_MONTH
    value_dict_total_time_work = ""

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.file_dict = self.load_file_time_work()




    def create_start_work_time(self,spinner):
        match spinner.uid:
            case  116:
                self.hours_start_work = spinner.text
                #print(spinner.uid,self.hours_start_work)
            case  157:
                self.minutes_start_work = spinner.text
                #print(spinner.uid, self.minutes_start_work)
            case  290:
                self.hours_end_work = spinner.text
                #print(spinner.uid, self.hours_end_work)
            case  331:
                self.minutes_end_work = spinner.text
                #print(spinner.uid, self.minutes_end_work)
            case  204:
                self.hours_start_lunch = spinner.text
                #print(spinner.uid, self.hours_start_lunch)
            case  245:
                self.minutes_start_lunch = spinner.text
                #print(spinner.uid, self.minutes_start_lunch)
            case  378:
                self.hours_end_lunch = spinner.text
                #print(spinner.uid, self.hours_end_lunch)
            case  419:
                self.minutes_end_lunch = spinner.text
                #print(spinner.uid, self.minutes_end_lunch)
        tuple_time = (self.hours_start_work, self.minutes_start_work, self.hours_end_work,
                    self.minutes_end_work, self.hours_start_lunch, self.minutes_start_lunch,
                    self.hours_end_lunch, self.minutes_end_lunch)

        self.work_time_calc(tuple_time)

    def write_file_time_work(self):
        print("До with")
        with open("data_base.dat", 'wb') as files:
            pickle.dump(self.file_dict, files)
            print("В with")
        print("После with")
        self.label_statistic.text = "def read_file_time_work"
        print("Сохранено")

    def load_file_time_work(self):
        try:
            with open("data_base.dat", 'rb') as f:
                self.file_dict = pickle.load(f)
        except (IOError,EOFError):
            with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass
        return {}


    def work_time_calc(self,args):
        """" В ф-ции расчитывается время отработки и
        формируется список значений для словаря.
        "4:33" часы, минуты"""
        Hour_start_work = int(args[0])
        Min_start_work = int(args[1])

        Hour_end_work = int(args[2])
        Min_end_work = int(args[3])

        Hour_start_lunch = int(args[4])
        Min_start_lunch = int(args[5])
        Hour_end_lunch = int(args[6])
        Min_end_lunch = int(args[7])

        time_start_lunch = timedelta(hours=Hour_start_lunch, minutes=Min_start_lunch)
        time_end_lunch = timedelta(hours=Hour_end_lunch, minutes=Min_end_lunch)
        total_time_lunch = time_end_lunch - time_start_lunch


        time_start_work = timedelta(hours=Hour_start_work,minutes=Min_start_work)
        time_end_work = timedelta(hours=Hour_end_work,minutes=Min_end_work)
        total_time_work = (time_end_work - time_start_work) - total_time_lunch
        print(total_time_work)
        if len(str(total_time_work)) == 8:
            self.total_hours_work = str(total_time_work)[:2]
        else:
            self.total_hours_work = str(total_time_work)[0]
        self.total_minutes_work = str(total_time_work)[-5:-3]
        self.value_dict_total_time_work = self.total_hours_work + ":" + self.total_minutes_work

    def create_a_date_for_label(self):
        """Формируется ключ для словаря
        key_dict_total_data = "10 Января" """
        self.label_month_lst_property.clear()
        day = self.ids['day'].text
        month = self.ids['month'].text
        self.label_month_lst_property.append(day)
        self.label_month_lst_property.append(month)
        self.key_dict_total_data = day + " " + month

    def validate_file_time_work(self):
        data = self.key_dict_total_data
        time_work = self.value_dict_total_time_work
        if data in self.file_dict:
            self.mypoput()
        else:
            self.file_dict[data] = time_work
            self.write_file_time_work()

    def overwriting(self):
        data = self.key_dict_total_data
        time_work = self.value_dict_total_time_work
        self.file_dict[data] = time_work
        self.write_file_time_work()

    def mypoput(self):
        def answer_ok(instance):
            if instance.text == "Ok":
                self.overwriting()
                mynepopup.dismiss()
            elif instance.text == "Cancel":
                mynepopup.dismiss()
        mynepopup = Popup(title = "Info",size_hint = (.8, .4))
        container = FloatLayout(size_hint=(1, 1))
        lab = Label(text="Рабочий день на эту дату существует.\n Переписать?",
                    font_size=30, size_hint=(1, .3), pos_hint={'x': .001, 'top': 1},
                    halign='center')
        container.add_widget(lab)
        btn_ok = Button(text="Ok", size_hint=(.3, .3),
                        pos_hint={'x': .15, 'y': .1})
        btn_ok.bind(on_press=answer_ok)
        container.add_widget(btn_ok)
        btn_cancel = Button(text="Cancel", size_hint=(.3, .3),
                            pos_hint={'x': .55, 'y': .1})
        btn_cancel.bind(on_press=answer_ok)
        container.add_widget(btn_cancel)
        mynepopup.content = container
        mynepopup.open()  # Запустить Poput













class MyApp(App):
    def build(self):
        return Pages()
    def on_start(self):
        pass

    def quit_program(self):
        exit()

if __name__ == '__main__':
    MyApp().run()
