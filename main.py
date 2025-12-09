# if not os.path.isfile("data_base.dat"):  # создание на HDD файла, если нету
        # with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass
# class MyList(list):
#     def __getitem__ (self, offset):
#         return list.__getitem__ (self, offset - 1)
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
from kivy.properties import ListProperty,StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

def install_time_in_stringproperty():
    directory = os.path.dirname(os.path.abspath(__file__))
    try:
        with open("file_save_time.txt") as f:
            file_open = f.readlines()
    except (FileNotFoundError,ValueError):
        with open(os.path.join(directory,"file_save_time.txt"), "w") as file_open:
            for i in range(8):
                file_open.write("00" + "\n")
            file_open.write("normal")
        with open("file_save_time.txt") as f:
            file_open = f.readlines()
    return file_open

INSTALL_TIME = [x.rstrip() for x in install_time_in_stringproperty()]

"""Установить kv файл в директорию совместно в main.py"""
dir_name = os.path.split(os.path.abspath(__file__))
Builder.load_file(os.path.join(dir_name[0], "main_kv.kv"))

month_lst = ['Январь', 'Февраль', 'Март', 'Апрель','Май', 'Июнь',
             'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

time_now = time.time() # Секунды с начала эпохи
time_day = time.localtime(time_now) # Текущее число

if time.strftime("%d", time_day)[0] == "0":
    CURRENT_DAY = time.strftime("%d", time_day)[1]
else:
    CURRENT_DAY = time.strftime("%d", time_day)

number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]





class Pages(Carousel):
    """Читай переменные. Их имена обо всём говорят."""
    hours_start_work = StringProperty(INSTALL_TIME[0])
    minutes_start_work = StringProperty(INSTALL_TIME[1])

    hours_end_work = StringProperty(INSTALL_TIME[2])
    minutes_end_work = StringProperty(INSTALL_TIME[3])

    hours_start_lunch = StringProperty(INSTALL_TIME[4])
    minutes_start_lunch = StringProperty(INSTALL_TIME[5])

    hours_end_lunch = StringProperty(INSTALL_TIME[6])
    minutes_end_lunch = StringProperty(INSTALL_TIME[7])

    total_hours_work = StringProperty("00")
    total_minutes_work = StringProperty("00")

    from_total_days_spinner = StringProperty("")
    total_month_spinner = StringProperty(CURRENT_MONTH)
    to_total_days_spinner = StringProperty("")

    total_hours_work_statistic = StringProperty()
    total_minutes_work_statistic = StringProperty()

    list_from_total_days = ListProperty()
    list_to_total_days = ListProperty()

    lab_save_txt = StringProperty("Отработано:")

    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)

    spinner_month_lst = ListProperty(month_lst)
    spinner_month_statistic_lst = ListProperty()  # Устан.всех месяцев в Spinner

    spinner_statistic_month_lst = ListProperty([])  # Устан.всех месяцев в Spinner

    label_month_lst = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label

    key_dict_total_data = CURRENT_DAY + " " + CURRENT_MONTH

    def __init__(self, **kwargs):
        super(Pages, self).__init__(**kwargs)
        self.load_slide(self.next_slide)  ##################### следущий Pages
        self.ids["check_save_time"].state = INSTALL_TIME[8]
        self.value_dict_total_time_work = "0:0"
        self.all_work_num_days_for_statistic = [] # Рабочие дни выбранного месяца
        self.all_month_for_statistic = [] # Все месяцы из словаря
        self.keys_all_work_data_sorted = []
        self.file_dict = {}
        self.main()

    def main(self):
        self.file_dict = self.load_file_time_work() # Загрузка с HDD словаря
        self.update_statistic()
        if "down" in INSTALL_TIME:
            self.install_total_time_after_save()

    def install_total_time_after_save(self):
        tuple_time = (self.hours_start_work, self.minutes_start_work, self.hours_end_work,
                      self.minutes_end_work, self.hours_start_lunch, self.minutes_start_lunch,
                      self.hours_end_lunch, self.minutes_end_lunch)
        self.work_time_calc(tuple_time)

    def update_statistic(self,choice_month:str=CURRENT_MONTH):
        lst_dates_current_month = self.get_dates_from_current_month(choice_month) # Список дат с нужным месяцем
        lst_sorted_num_current_month = self.get_num_days(lst_dates_current_month) # Список чисел нужного месяца
        lst_keys_dates = self.create_keys_date_choice_month(lst_sorted_num_current_month) # Список ["10 Октябрь"]
        time_statistic = self.update_total_time_statistic(lst_keys_dates) # Кортеж (170,45) часы минуты
        lst_all_month = self.get_set_all_month()

        self.install_statistic(lst_sorted_num_current_month,lst_all_month,time_statistic,choice_month)

    def install_statistic(self,*args):
        self.spinner_month_statistic_lst = args[1] # Устан.всех месяцев в Spinner
        self.total_month_spinner = args[3]  # Устан.выбранного месяца в Spinner
        try:
            self.from_total_days_spinner = str(args[0][0])  # Первое число месяца
            self.to_total_days_spinner = str(args[0][-1])  # Последнее число месяца
        except IndexError:
            self.from_total_days_spinner = "0" # Первое число месяца, если словарь пустой!
            self.to_total_days_spinner = "0"   # Последнее число месяца, если словарь пустой!

        self.list_from_total_days = map(str, args[0])  # Установка списка чисел
        self.list_to_total_days = map(str, args[0])  # Установка списка чисел
        self.total_hours_work_statistic = args[2][0] # Установка времени часы
        self.total_minutes_work_statistic = args[2][1] # Установка времени минуты

    def get_set_all_month(self):
        all_month = []
        for i in self.file_dict: # Получаем в i ключи словаря
            all_month.append(i.split()[1])
        return set(all_month)

    def get_dates_from_current_month(self, choice_month):
        list_month = []  # Только даты выбранного месяца
        for i in self.file_dict:  # Получаем в i ключи словаря
            if i.split()[1] == choice_month:  # Определяем нужный месяц из списка. Вычленяем название месяца
                list_month.append(i)  # Записываем в список только даты с нужным месяцем
        return list_month

    def get_num_days(self,lst_current_month:list):
        lst_num_days = []
        for i in lst_current_month: # Идём по списку месяца
            num_day = int(i.split()[0]) # Вычленяя только число месяца оборачивая в int()
            lst_num_days.append(num_day) # Только числа: int выбранного месяца
        lst_num_days.sort()
        return lst_num_days

    def create_keys_date_choice_month(self, sorted_num_current_days:list, month_choice:str=CURRENT_MONTH):
        keys_all_work = []
        for i in range(len(sorted_num_current_days)): # Проход по длинне списка дат
            keys_all_work.append(str(sorted_num_current_days[i]) + " " + month_choice) # создание строки ключа словаря и запись в список
        return keys_all_work

    def update_total_time_statistic(self,keys_all_work_data_sorted:list):
        hours = 0
        minutes = 0
        for i in keys_all_work_data_sorted: # ==========>>>>>>> ключи
            hours += int(self.file_dict[i].split(":")[0])
            minutes += int(self.file_dict[i].split(":")[1])

        hours_delta = timedelta(hours=hours).total_seconds()
        minutes_delta = timedelta(minutes=minutes).total_seconds()
        total_time_in_sec = minutes_delta + hours_delta
        hours_total = int(total_time_in_sec // 3600)
        minut = int((total_time_in_sec - hours_total * 3600) / 60)
        return str(hours_total), str(minut)

    def list_sort_choices_num_days(self,list_num_choice_month,firstday,lastday):
        list_num_choice = []
        for i in list_num_choice_month:
            if int(firstday) <= i <= int(lastday):
                list_num_choice.append(i)
        return list_num_choice

    def create_choice_spinner(self, spinner):
        match spinner.uid:
            case 3581:
                self.from_total_days_spinner = spinner.text
                if self.total_month_spinner != '' and  self.to_total_days_spinner != '':
                    self.statistic_from_spinner(self.total_month_spinner)
            case 3617:
                self.total_month_spinner = spinner.text
                if self.from_total_days_spinner != '' and  self.to_total_days_spinner != '':
                    self.install_firsday_lastday(self.total_month_spinner)
                    self.statistic_from_spinner(self.total_month_spinner)
            case 3653:
                self.to_total_days_spinner = spinner.text
                if self.from_total_days_spinner != '' and self.total_month_spinner != '':
                    self.statistic_from_spinner(self.total_month_spinner)

    def install_firsday_lastday(self,c_month):
        """Устанавливает первый и последний день выбранного месяца после выбора spinner месяца"""
        lst_dates_choice_month = self.get_dates_from_current_month(c_month)  # Получаем даты с нужным месяцем list
        sort_num_choice = self.get_num_days(lst_dates_choice_month)  # Список int выбранных чисел для Spinner

        self.from_total_days_spinner = str(sort_num_choice[0])
        self.to_total_days_spinner = str(sort_num_choice[-1])

    def statistic_from_spinner(self,choice_month):
        lst_dates_choice_month = self.get_dates_from_current_month(choice_month) # Получаем даты с нужным месяцем list
        sort_num_choice = self.get_num_days(lst_dates_choice_month) # Список int выбранных чисел для Spinner

        list_sort_num_choice = self.list_sort_choices_num_days(sort_num_choice,self.from_total_days_spinner,
                                                               self.to_total_days_spinner)
        lst_keys_choice_date = self.create_keys_date_choice_month(list_sort_num_choice,choice_month)
        time_statistic = self.update_total_time_statistic(lst_keys_choice_date)  # Получаем кортеж (170,45) часы минуты
        self.install_totaltime_statistic(sort_num_choice,time_statistic)

    def install_totaltime_statistic(self,sort_num_choice, totaltime):
        self.list_from_total_days = map(str, sort_num_choice) # Установка списка чисел
        self.list_to_total_days = map(str, sort_num_choice)  # Установка списка чисел

        self.total_hours_work_statistic = str(totaltime[0])  # Установка времени часы
        self.total_minutes_work_statistic = str(totaltime[1])  # Установка времени минуты

    def get_from_current_month(self, choice_month,firstday,lastday):
        list_dates = self.get_dates_from_current_month(choice_month) # даты выбранного месяца List
        list_num_choice_month = self.get_num_days(list_dates) # Список чисел выбранного месяца List
        list_keys = self.create_keys_date_choice_month(list_num_choice_month,choice_month) # Список ключей
        return list_keys

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

        self.ids["check_save_time"].state = "normal"
        tuple_time = (self.hours_start_work, self.minutes_start_work, self.hours_end_work,
                    self.minutes_end_work, self.hours_start_lunch, self.minutes_start_lunch,
                    self.hours_end_lunch, self.minutes_end_lunch)
        self.work_time_calc(tuple_time)

    def my_callback(self,instance):
        self.lab_save_txt = "Отработано:"
        return False

    def write_file_time_work(self):
        with open("data_base.dat", 'wb') as files:
            pickle.dump(self.file_dict, files)
        Clock.schedule_once(self.my_callback, 2)
        self.lab_save_txt = "Сохранено"
        self.update_statistic()
        print(self.file_dict)


    def load_file_time_work(self):
        try:
            with open("data_base.dat", 'rb') as file:
                file_dict = pickle.load(file)
                print("Открыт успешно",file_dict)

        except (IOError,EOFError,FileNotFoundError):
            print("Не открылся. Создался пустой")
            with open(os.path.join(dir_name[0], "data_base.dat"), 'wb'): pass
            file_dict = {}

        return file_dict

    def work_less_day(self,time_args):
        Hour_start_work = int(time_args[0])
        Hour_end_work = int(time_args[2])
        Min_start_work = int(time_args[1])
        Min_end_work = int(time_args[3])

        Hour_start_lunch = int(time_args[4])
        Min_start_lunch = int(time_args[5])
        Hour_end_lunch = int(time_args[6])
        Min_end_lunch = int(time_args[7])

        time_start_lunch = timedelta(hours=Hour_start_lunch, minutes=Min_start_lunch)
        time_end_lunch = timedelta(hours=Hour_end_lunch, minutes=Min_end_lunch)
        total_time_lunch = time_end_lunch - time_start_lunch

        time_start_work = timedelta(hours=Hour_start_work, minutes=Min_start_work)
        time_end_work = timedelta(hours=Hour_end_work, minutes=Min_end_work)
        total_time_less_day_work = (time_end_work - time_start_work) - total_time_lunch

        return total_time_less_day_work

    def work_more_day(self,time_args):
        day = timedelta(hours=24)
        Hour_start_work = int(time_args[0])
        Hour_end_work = int(time_args[2])
        Min_start_work = int(time_args[1])
        Min_end_work = int(time_args[3])

        Hour_start_lunch = int(time_args[4])
        Min_start_lunch = int(time_args[5])
        Hour_end_lunch = int(time_args[6])
        Min_end_lunch = int(time_args[7])

        time_start_lunch = timedelta(hours=Hour_start_lunch, minutes=Min_start_lunch)
        time_end_lunch = timedelta(hours=Hour_end_lunch, minutes=Min_end_lunch)
        total_time_lunch = time_end_lunch - time_start_lunch

        time_start_work = timedelta(hours=Hour_start_work, minutes=Min_start_work)
        time_end_work = timedelta(hours=Hour_end_work, minutes=Min_end_work)

        diff_hours_with_day = day - time_start_work
        total = diff_hours_with_day + time_end_work

        total_time_more_day_work = total - total_time_lunch

        return total_time_more_day_work

    def work_time_calc(self, time_args):
        """" В ф-ции расчитывается время отработки """

        if int(time_args[0])>int(time_args[2]):
            total_time_work = self.work_more_day(time_args)
        else:
            total_time_work = self.work_less_day(time_args)
        self.create_value_for_dict(total_time_work)



    def create_value_for_dict(self,total_time_work):
        """self.value_dict_total_time_work = формируется строка значений для словаря.
        "4:33" часы, минуты"""
        if len(str(total_time_work)) == 8:
            self.total_hours_work = str(total_time_work)[:2]
        else:
            self.total_hours_work = str(total_time_work)[0]

        self.total_minutes_work = str(total_time_work)[-5:-3]
        self.value_dict_total_time_work = self.total_hours_work + ":" + self.total_minutes_work

    def create_a_date_for_label(self):
        """Формируется ключ для словаря
        key_dict_total_data = "10 Января" """
        self.label_month_lst.clear()
        day = self.ids['day'].text
        month = self.ids['month'].text
        self.label_month_lst.append(day)
        self.label_month_lst.append(month)
        self.key_dict_total_data = day + " " + month

    def validate_file_time_work(self):
        data = self.key_dict_total_data
        time_work = self.value_dict_total_time_work

        if data in self.file_dict:
            self.write_or_cancel_poput()
        else:
            self.file_dict[data] = time_work
            self.write_file_time_work()

    def overwriting(self):
        data = self.key_dict_total_data
        time_work = self.value_dict_total_time_work
        self.file_dict[data] = time_work
        self.write_file_time_work()

    def write_or_cancel_poput(self):
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
        return

    def btn_weekend(self):
        """Установка всех spinner в значение '00'- выходной день"""
        self.hours_start_work = "00"
        self.minutes_start_work = "00"
        self.hours_end_work = "00"
        self.minutes_end_work = "00"
        self.hours_start_lunch = "00"
        self.minutes_start_lunch = "00"
        self.hours_end_lunch = "00"
        self.minutes_end_lunch = "00"
        self.total_hours_work = "00"
        self.total_minutes_work = "00"

    def remember_the_time(self, value):
        CONDITION = self.ids["check_save_time"].state
        if value:
            self.record_value_time_in_file(CONDITION)
        else:
            self.record_value_time_in_file(CONDITION,FLAG=False)

    def record_value_time_in_file(self,condition,FLAG=True):
        if FLAG:
            with open("tests/file_save_time.txt", "w") as f:
                f.write(self.hours_start_work + "\n") # Индекс 0
                f.write(self.minutes_start_work + "\n") # Индекс 1
                f.write(self.hours_end_work + "\n") # Индекс 2
                f.write(self.minutes_end_work + "\n") # Индекс 3
                f.write(self.hours_start_lunch + "\n") # Индекс 4
                f.write(self.minutes_start_lunch + "\n") # Индекс 5
                f.write(self.hours_end_lunch + "\n") # Индекс 6
                f.write(self.minutes_end_lunch + "\n") # Индекс 7
                f.write(condition)
        else:
            with open("tests/file_save_time.txt", "w") as f:
                for i in range(8):
                    f.write("00" + "\n")
                f.write(condition)














class MyApp(App):
    def build(self):
        self.title = "Паши дурачёк, получишь значёк"
        Window.clearcolor = (.8, .8, .8)

        return Pages()

    def quit_program(self):
        exit()

if __name__ == '__main__':
    MyApp().run()
