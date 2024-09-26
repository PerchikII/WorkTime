#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random as rd
import info_text

from kivy.app import App

from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

Builder.load_file('Layouts_example.kv')


class MyButton(Button):
    def __init__(self, text, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.text = text
class MyScatter(Scatter):
    def __init__(self, size: tuple, pos: tuple, label_text: str, **kwargs):
        super(MyScatter, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.scale_min = .5
        self.scale_max = 5
        self.size = size
        self.pos = pos
        self.rotation = 60
        self.label_text = label_text
        lab = Label(text=self.label_text,color=(0,0,1,1),font_size=20)
        self.add_widget(lab)
    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            if touch.button == 'scrolldown':
                if self.scale < 10:
                    self.scale = self.scale * 1.1
            elif touch.button == 'scrollup':
                if self.scale > 1:
                    self.scale = self.scale * 0.8
            return True
        else:
            super(MyScatter,self).on_touch_down(touch)

class My_Pop(Popup):
    def __init__(self, text, **kwargs):
        super(My_Pop, self).__init__(**kwargs)

        self.title = "Info"
        self.text = text
        self.size_hint = (1, 1)
        container = FloatLayout(size_hint=(1, 1))

        lab = Label(text=self.text, font_size=20, markup=True,
                    size_hint=(1, .8), pos_hint={'x': .001, 'top': 1},
                    halign='center')
        container.add_widget(lab)
        btn = MyButton("Закрыть", size_hint=(.2, .1),
                       pos_hint={'center_x': .5, 'y': .1},
                       on_press=self.dismiss)
        container.add_widget(btn)
        self.content = container
        self.open()


class Main(Screen):
    showcoord_btn = StringProperty('[color=#03fcb1]FloatLayout[/color]\nсовмесно со [color=#03fcb1]ScrollView[/color] widget')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(30):
            self.btn = Button(size_hint=(None, None), size=(100, 50),
                              on_press=self.show_coord)
            self.btn.pos = self.pos_button()
            self.btn.text = f'x={self.btn.pos[0]}\ny={self.btn.pos[1]}'
            self.ids.my_box.add_widget(self.btn)

    def pos_button(self):
        x = rd.randint(50, 500)
        y = rd.randint(100, 1000)
        return (x, y)

    def show_coord(self, touch):
        self.showcoord_btn = (f'Я кнопка с координатами\n'
                              f'x={touch.pos[0]}\ny={touch.pos[1]}')

    def create_info(self):
        """Создание Popup окна с информацией"""
        My_Pop(info_text.TXT_Screen_Main)


class Second(Screen):
    change_orient_box = StringProperty('horizontal')
    orient_box = StringProperty(f'Это [color=#e85b58][b]горизонтальный[/b][/color] BoxLayout')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_orient(self):
        if self.orient_box[22] == 'г':
            self.orient_box = 'Это [color=#e85b58][b]вертикальный[/b][/color] BoxLayout'
            self.change_orient_box = 'vertical'

        else:
            self.orient_box = 'Это [color=#e85b58][b]горизонтальный[/b][/color] BoxLayout'
            self.change_orient_box = 'horizontal'

    def create_info(self):
        """Создание Popup окна с информацией"""
        My_Pop(info_text.TXT_Screen_Second)



class Third(Screen):
    def __init__(self, **kwargs):
        super(Third, self).__init__(**kwargs)
        self.add_widget(MyScatter((100, 100), (250, 170), 'Hello'))

    def create_info(self):
        """Создание Popup окна с информацией"""
        My_Pop(info_text.TXT_Screen_Third)

class MyGridLayout(GridLayout):
    def __init__(self,**kwargs):
        super(MyGridLayout,self).__init__(**kwargs)
        self.calculate_list = []
        self.cols = 3
        self.grid_label = Label(text='',font_size=40)
        self.grid_label.color = '##54ff9f'
        self.add_widget(self.grid_label)
        for i in range(1,7):
            btn = Button(text=f'{i}',font_size=50,
                         on_press=self.pressfunc)
            self.add_widget(btn)
    def pressfunc(self,instance):
        c_list = self.calculate_list
        c_list.append(instance.text)
        self.grid_label.text = ''
        self.grid_label.text = ''.join(c_list)
        print(c_list)
        if len(c_list) == 3 and c_list[1] == '+':
            print(c_list, c_list[1])
            self.grid_label.text = str(eval('+'.join(c_list)))
            c_list.clear()
        elif len(c_list) == 3 and c_list[1] == '-':
            print(c_list, c_list[1])
            self.grid_label.text = str(eval('-'.join(c_list)))
            c_list.clear()
        elif len(c_list) == 3:
            c_list.clear()

    def clear_calc(self):
        self.grid_label.text = '0'
        self.calculate_list.clear()

class Fourth(Screen):
    def __init__(self,**kwargs):
        super(Fourth,self).__init__(**kwargs)
        # lst = [x for x in self.walk()]
        # print(lst[5].text)
        # lst[5].text='333333'

    def create_info(self):
        """Создание Popup окна с информацией"""
        My_Pop(info_text.TXT_Screen_Fourth)

class Layouts_exampleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main(name='first'))
        sm.add_widget(Second(name='second'))
        sm.add_widget(Third(name='third'))
        sm.add_widget(Fourth(name='fourth'))
        sm.current = "fourth"
        return sm


if __name__ == "__main__":
    Layouts_exampleApp().run()
