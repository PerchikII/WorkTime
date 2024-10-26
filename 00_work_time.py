import time
import os
from calendar import month
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


# class MyList(list):
#     def __getitem__ (self, offset):
#         return list.__getitem__ (self, offset - 1)

"""Установить kv файл в директорию совместно в main.py"""
dirname = os.path.split(os.path.abspath(__file__))
Builder.load_file(os.path.join(dirname[0],"00_work_time.kv"))

month_lst = ['Января', 'Февраля', 'Марта', 'Апреля','Мая', 'Июня',
             'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']

time_now = time.time() # Секунды с начала эпохи
time_day = time.localtime(time_now) # Текущее число

if time.strftime("%d", time_day)[0] == "0":
    CURRENT_DAY = time.strftime("%d", time_day)[1]
else:
    CURRENT_DAY = time.strftime("%d", time_day)

number_month = int(time.strftime("%m", time_day))
CURRENT_MONTH = month_lst[number_month - 1]

# CURRENT_HOURS = time.strftime("%H", time_day)
# CURRENT_MINUTES = time.strftime("%M", time_day)

# if not os.path.isfile("data_base.dat"):  # создание на HDD файла, если нету
        # with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass

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

    from_total_days_spinner = StringProperty("1") ##########################################
    from_total_month_spinner = StringProperty(CURRENT_MONTH) ##########################################
    to_total_days_spinner = StringProperty("0") ############################################

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
        self.load_slide(self.next_slide)  ######### следущий Pages

        self.value_dict_total_time_work = "0:0"

        self.all_work_num_days_for_statistic = [] # Рабочие дни выбранного месяца
        self.all_month_for_statistic = [] # Все месяцы из словаря

        self.keys_all_work_data_sorted = []
        self.file_dict = {}
        self.main()

    def main(self):
        self.file_dict = self.load_file_time_work() # Загрузка с HDD словаря
        self.sort_file_dict() # Сортировка

    def install_statistic(self, month_choice:str,hours_stat:str,minutes_stat:str):
        self.spinner_month_statistic_lst = self.all_month_for_statistic # list
        self.from_total_month_spinner = month_choice


        self.from_total_days_spinner = str(self.all_work_num_days_for_statistic[0])  # Первое число месяца
        self.list_from_total_days = map(str, self.all_work_num_days_for_statistic)  # Установка списка чисел

        self.to_total_days_spinner = str(self.all_work_num_days_for_statistic[-1])  # Последнее число месяца

        self.list_to_total_days = map(str, self.all_work_num_days_for_statistic)  # Установка списка чисел

        self.total_hours_work_statistic = hours_stat
        self.total_minutes_work_statistic = minutes_stat



    def update_statistic(self,month_choice):
        """Установка данных для статистики
        число 1-го рабочего дня текущего месяца и последний раб день"""
        all_month_for_statistic = []
        for i in self.file_dict: # Получаем в i ключи словаря
            all_month_for_statistic.append(i.split()[1])
        self.all_month_for_statistic = set(all_month_for_statistic)

        time_statistic = self.update_total_time_statistic(self.keys_all_work_data_sorted)
        hours_stat = time_statistic[0]
        minutes_stat = time_statistic[1]
        self.install_statistic(month_choice,hours_stat,minutes_stat)

    def update_total_time_statistic(self,keys_all_work_data_sorted):
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

    def sort_file_dict(self, choice_month:str=CURRENT_MONTH,firstday=None,lastday=None, FLAG=True):
        get_list_month = [] # Только даты выбранного месяца

        for i in self.file_dict: # Получаем в i ключи словаря
            if i.split()[1] == choice_month: # Определяем нужный месяц из списка. Вычленяем название месаца
                get_list_month.append(i) # Записываем в список только даты с нужным месяцем
        self.all_work_num_days_for_statistic.clear()
        if FLAG:
            for i in get_list_month: # Идём по списку месяца
                num_day = int(i.split()[0]) # Вычленяя только число месяца оборачивая в int()
                self.all_work_num_days_for_statistic.append(num_day) # Только числа: int выбранного месяца
        else:
            for i in get_list_month:
                num_day = int(i.split()[0])
                if int(firstday) <= num_day <= int(lastday):
                    self.all_work_num_days_for_statistic.append(num_day)

        self.all_work_num_days_for_statistic.sort() # Сортировка списка чисел месяца
        self.keys_all_work_data_sorted.clear()
        for i in range(len(self.all_work_num_days_for_statistic)): # Проход по длинне списка дат
            self.keys_all_work_data_sorted.append(str(self.all_work_num_days_for_statistic[i]) + " " + choice_month) # создание строки ключа словаря и запись в список

        self.update_statistic(choice_month) # Обновление статистики






    def create_statistic_date(self,spinner):
        print("Запуск create_statistic_date()")
        match spinner.uid:
            case 3557:
                self.from_total_days_spinner = spinner.text

                #print(self.from_total_days_spinner)
            case 3593:
                self.from_total_month_spinner = spinner.text

                #print(self.from_total_month_spinner)
            case 3629:
                self.to_total_days_spinner = spinner.text
                #print(self.to_total_days_spinner)

        #self.sort_file_dict(month_choice,first_day,last_day,FLAG=False)

    def sort_statistic(self,file_dict,month_statistic,firstday,lastday):
        get_list_month = []  # Только даты выбранного месяца
        num_days_lst =[]
        list_keys_for_statistic = []

        for i in file_dict:  # Получаем в i ключи словаря
            if i.split()[1] == month_statistic:  # Определяем нужный месяц из списка. Вычленяем название месаца
                get_list_month.append(i)  # Записываем в список только даты с нужным месяцем
        for i in get_list_month:  # Идём по списку месяцев
            num_day = int(i.split()[0])  # Вычленяя только число месяца оборачивая в int()
            num_days_lst.append(num_day)

        for i in sorted(num_days_lst):
            if int(firstday) <= i <= int(lastday):
                list_keys_for_statistic.append(str(i)+ " "+month_statistic)

        time_statistic = self.update_total_time_statistic(list_keys_for_statistic)
        self.total_hours_work_statistic = time_statistic[0]
        self.total_minutes_work_statistic = time_statistic[1]


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

    def my_callback(self,instance):
        self.lab_save_txt = "Отработано:"
        return False

    def write_file_time_work(self):
        with open("data_base.dat", 'wb') as files:
            pickle.dump(self.file_dict, files)
        Clock.schedule_once(self.my_callback, 2)
        self.lab_save_txt = "Сохранено"
        print("Сохранено")
        self.sort_file_dict()
        print(self.file_dict)
        print("++++++++++++++++++++++++++++++++++++++++++++++++")

    def load_file_time_work(self):
        try:
            with open("data_base.dat", 'rb') as file:
                file_dict = pickle.load(file)
                print("Открыт успешно",file_dict)
                print("===========================================")
        except (IOError,EOFError,FileNotFoundError):
            print("Не открылся. Создался пустой")
            with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass
            file_dict = {}
            print(self.file_dict)
        return file_dict

    def work_time_calc(self,args):
        """" В ф-ции расчитывается время отработки """

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













class MyApp(App):
    def build(self):
        self.title = "Паши дурачёк, получишь значёк"
        Window.clearcolor = (.8, .8, .8)

        return Pages()

    def quit_program(self):
        exit()

if __name__ == '__main__':
    MyApp().run()
