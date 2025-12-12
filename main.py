# if not os.path.isfile("data_base.dat"):  # создание на HDD файла, если нету
        # with open(os.path.join(dirname[0], "data_base.dat"), 'wb'): pass
# class MyList(list):
#     def __getitem__ (self, offset):
#         return list.__getitem__ (self, offset - 1)
import time
import os
from datetime import timedelta
import pickle
from pprint import pprint

from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField


from kivy.lang.builder import Builder
from kivy.properties import ListProperty,StringProperty
from kivy.clock import Clock
from kivy.core.window import Window

# def install_time_in_stringproperty():
#     directory = os.path.dirname(os.path.abspath(__file__))
#     try:
#         with open("file_save_time.txt") as f:
#             file_open = f.readlines()
#     except (FileNotFoundError,ValueError):
#         with open(os.path.join(directory,"file_save_time.txt"), "w") as file_open:
#             for i in range(8):
#                 file_open.write("00" + "\n")
#             file_open.write("normal")
#         with open("file_save_time.txt") as f:
#             file_open = f.readlines()
#     return file_open
#
# INSTALL_TIME = [x.rstrip() for x in install_time_in_stringproperty()]

dir_name = os.path.split(os.path.abspath(__file__))
def load_HDDfile():
    try:
        with open("statistic_data.dat", 'rb') as file:
            file_dict = pickle.load(file)
            return file_dict
    except (FileNotFoundError, IOError, EOFError):
        # Код одноразовый для первого запуска программы
        print("Не открылся. Создался пустой")
        with open(os.path.join(dir_name[0], "statistic_data.dat"), 'wb') as obj:
            file_dict = {}
            pickle.dump(file_dict, obj)
    return file_dict

def save_HDD_DICT_TIME(dictionary,name_file):
    with open("worktime_data.dat", 'wb') as file:
        pickle.dump(dictionary, file)

DICT_TIME_STATISTIC = load_HDDfile()
# DICT_ROUT = load_HDDfile()




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


class PagesManager(MDScreenManager):
    def __init__(self, **kwargs):
        MDScreenManager.__init__(self, **kwargs)
    def on_touch_down(self, touch):
        self.tap_X_Down = touch.x
        self.tap_Y_Down = touch.y
        return super(PagesManager, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        self.tap_X_Up = touch.x
        self.tap_Y_Up = touch.y
        if (self.tap_X_Down - self.tap_X_Up) > 100:
            if self.current == "main_page":
               self.transition.direction = "left"
               self.current = "stat_page"
               self.transition = SlideTransition()
        if self.tap_X_Down < self.tap_X_Up:
             if  self.current == "stat_page":
                 self.transition.direction = "right"
                 self.current = "main_page"
                 self.transition = SlideTransition()
        if (self.tap_Y_Down - self.tap_Y_Up) > 100:
            if self.current == "main_page":
                self.transition.direction = "down"
                self.current = "sett_page"
        return super(PagesManager, self).on_touch_up(touch)
class Pages_main(MDScreen):
    """Читай переменные. Их имена обо всём говорят."""
    day_spinner = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)
    month_spinner_lst = ListProperty(month_lst)

    hours_start_lunch = StringProperty("00")
    minutes_start_lunch = StringProperty("00")

    hours_end_lunch = StringProperty("00")
    minutes_end_lunch = StringProperty("00")

    hours_start_work = StringProperty("00")
    minutes_start_work = StringProperty("00")

    hours_end_work = StringProperty("00")
    minutes_end_work = StringProperty("00")

    total_hours_work = StringProperty("00")
    total_minutes_work = StringProperty("00")

    date_total_time = StringProperty(CURRENT_DAY + " " + CURRENT_MONTH)

    lab_save_txt = StringProperty("Отработано:")
    key_dict_total_data = CURRENT_DAY + " " + CURRENT_MONTH

    def __init__(self, **kwargs):
        MDScreen.__init__(self,**kwargs)
        self.route_and_time = ["route",()]
        #self.main()

    def main(self):
        self.update_statistic()
        if "down" in INSTALL_TIME:
            self.install_total_time_after_save()

    def intercept_data_main_screen(self):
        date_choice_user:str = self.get_user_choice_date()
        total_time:tuple[str,str] = self.get_total_time_in_a_day()
        route_and_karta_in_day:str = self.get_route_user_choice()

        self.save_date_in_time_dict(date_choice_user,route_and_karta_in_day,total_time)


        # print(date_choice_user,route_and_karta_in_day,total_time)

    def save_date_in_time_dict(self,key:str,route:str,tot_time:tuple[str,str]):

        self.route_and_time[0] = route
        self.route_and_time[1] = tot_time
        DICT_TIME_STATISTIC[key] = self.route_and_time
        # self.save_date_in_HDD(DICT_TIME_STATISTIC)
        pprint(DICT_TIME_STATISTIC)


    @staticmethod
    def save_date_in_HDD(global_dict):
        save_HDD_DICT_TIME(global_dict,"worktime_data.dat")


    def get_route_user_choice(self):
        route = self.ids["route_number_textinput"].text
        karta = self.ids["karta_route_number_textinput"].text
        if route and karta:
            return route + "/" + karta
        else:
            return "Не введён"



    def get_total_time_in_a_day(self):
        hours = self.total_hours_work
        mitutes = self.total_minutes_work
        return hours,mitutes


    def get_user_choice_date(self):
        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        return day + " " + month







    def start_calculate_work_time(self):
        # Начало раб.дня
        start_work_H = self.ids["startworkhours"].text
        start_work_M = self.ids["startworkminutes"].text
        # Конец раб.дня
        end_work_H = self.ids["hoursendwork"].text
        end_work_M = self.ids["minutesendwork"].text
        # Обед начало
        start_lunch_H = self.ids["hoursstartlunch"].text
        start_lunch_M = self.ids["minutesstartlunch"].text
        # Обед конец
        end_lunch_H = self.ids["hoursendlunch"].text
        end_lunch_M = self.ids["minutesendlunch"].text

        time_tuple = (start_work_H,start_work_M,end_work_H,end_work_M,start_lunch_H,start_lunch_M,end_lunch_H,end_lunch_M)
        if int(start_work_H) > int(end_work_H):
            total_time_work = self.calculate_time_more_day(time_tuple)
        else:
            total_time_work = self.calculate_time_less_day(time_tuple)
        self.install_total_time_work_in_label(total_time_work)
    def install_total_time_work_in_label(self,total_time_work):
        time_struct = time.gmtime(total_time_work.total_seconds())
        self.total_hours_work = str(time_struct.tm_hour)
        self.total_minutes_work = str(time_struct.tm_min)
        day = self.ids["spinner_day"].text
        month = self.ids["spinner_month"].text
        self.date_total_time = day+ " "+ month
    @staticmethod
    def calculate_time_more_day(time_tuple):
        day = timedelta(hours=24)
        Hour_start_work = int(time_tuple[0])
        Hour_end_work = int(time_tuple[2])
        Min_start_work = int(time_tuple[1])
        Min_end_work = int(time_tuple[3])

        Hour_start_lunch = int(time_tuple[4])
        Min_start_lunch = int(time_tuple[5])
        Hour_end_lunch = int(time_tuple[6])
        Min_end_lunch = int(time_tuple[7])

        time_start_lunch = timedelta(hours=Hour_start_lunch, minutes=Min_start_lunch)
        time_end_lunch = timedelta(hours=Hour_end_lunch, minutes=Min_end_lunch)
        total_time_lunch = time_end_lunch - time_start_lunch

        time_start_work = timedelta(hours=Hour_start_work, minutes=Min_start_work)
        time_end_work = timedelta(hours=Hour_end_work, minutes=Min_end_work)

        diff_hours_with_day = day - time_start_work
        total = diff_hours_with_day + time_end_work
        total_time_more_day_work = total - total_time_lunch
        return total_time_more_day_work
    @staticmethod
    def calculate_time_less_day(time_args):
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
        lab = MDLabel(text="Рабочий день на эту дату существует.\n Переписать?",
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

class Pages_stat(MDScreen):
    """Читай переменные. Их имена обо всём говорят."""
    from_total_days_spinner = StringProperty("")
    total_month_spinner = StringProperty(CURRENT_MONTH)
    to_total_days_spinner = StringProperty("")

    total_hours_work_statistic = StringProperty()
    total_minutes_work_statistic = StringProperty()

    list_from_total_days = ListProperty()
    list_to_total_days = ListProperty()

    day_spinner_str = StringProperty(CURRENT_DAY)
    month_spinner_str = StringProperty(CURRENT_MONTH)

    label_month_lst = ListProperty([CURRENT_DAY, CURRENT_MONTH])  # Устан.даты в Label

    spinner_month_statistic_lst = ListProperty()  # Устан.всех месяцев в Spinner


    def __init__(self, **kwargs):
        MDScreen.__init__(self,**kwargs)







class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Light Dark
        self.theme_cls.primary_palette = "Olive"  # "Teal" #"Purple" # , "Red" "Olive"
        # Window.clearcolor = (.8, .8, .8)
        Builder.load_file(os.path.join(dir_name[0], "main_kv.kv"))
        scm = PagesManager()
        scm.add_widget(Pages_main())
        scm.add_widget(Pages_stat())
        return scm
    def quit_program(self):
        exit()

class RouteTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 3:
                return super().insert_text(value, from_undo=from_undo)
class KartaTextInput(MDTextField):
    def __init__(self, **kwargs):
        MDTextField.__init__(self, **kwargs)
    def insert_text(self, value, from_undo=False):
        if value.isdigit():
            if len(self.text) < 2:
                return super().insert_text(value, from_undo=from_undo)

if __name__ == '__main__':
    MyApp().run()
