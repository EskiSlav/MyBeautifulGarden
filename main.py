# Работа должна быть выполнена на python обязательно(и только) по принципам ооп - 
# полиморфизм, инкапсуляция, наследование, вывести все это через gui, например 
# tkinter, программа также должна работать с небольшой базой данный типа sql или postgres. 
# итогом курсовой работы должна стать рабочая программа с интерфейсом. описание взаимодействия 
# классов функций и методов должно быть детальное.

# Тема потрібної курсової роботи

#  «Мій прекрасний сад» 
# Основні класи: рослина (назва рослини, тип рослини, фото, посилання на файл з описом, 
# температурний режим, режим поливу, режим освітлення, період цвітіння), список рослин. 
# Основні функції: ведення списку рослин, пошук рослини за різними ознаками, ведення довідника 
# типів рослин, типів режимів поливу та освітлення. 

# Щодо самої роботи, точніше її практичної частини. Потрібно написати програму на Python з GUI. 
# Це курсова робота по ООП, тож обов'язково треба спроектувати класи, бази даних не треба, 
# тільки потрібно заповнити декілька рослин щоб було зрозуміло що і як працює. 
# В описі програми обов'язково вказати(постановка задачі), де і як ми використовуємо наслідування, 
# поліморфізм та інкапсуляцію. Опис функцій, схема взаємодії, структура проекту, повний лістинг самої програми

import logging
import tkinter as tk

from mytypes import *

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Application(tk.Frame):
    def __init__(self, master=None):
        
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.LEFT = 300
        self.RIGHT = 300
        master.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.LEFT}+{self.RIGHT}")

        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_btn = tk.Button(self.master, text='Select')
        self.select_btn['command'] = self.select_from_db
        self.select_btn.place(x=int(self.WIDTH/4 - 50), y=int(3*self.HEIGHT/4), width=100)

        self.text_field = tk.Text(self.master, width=67, height=36, state=tk.DISABLED)
        self.text_field.place(x=self.WIDTH/2 + 10, y=10) 

        offset = 0
        self.name_label = tk.Label(self.master, text='Название растения')
        self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)

        # offset = 15
        # self.name_label = tk.Label(self.master, text='Тип растения')
        # self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        # self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        # self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)

        # offset = 30
        # self.name_label = tk.Label(self.master, text='Температурный режим')
        # self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        # self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        # self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)

        # offset = 45
        # self.name_label = tk.Label(self.master, text='Режим Полива')
        # self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        # self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        # self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)

        # offset = 60
        # self.name_label = tk.Label(self.master, text='Режим Освещения')
        # self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        # self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        # self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)

        # offset = 75
        # self.name_label = tk.Label(self.master, text='Период цветения')
        # self.name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        # self.name_field.place(x=150, y=int(self.HEIGHT/2) + offset)
        # self.name_label.place(x=10, y=int(self.HEIGHT/2) - 2 + offset)



    def select_from_db(self):
        plant_name = self.name_field.get("1.0", tk.END)[:-1]
        # plant_name = self.name_field.get() # ???

        if len(plant_name) > 0:
            query = (Plant.select()
                     .join(PlantType, on=(PlantType.plant_type_id == Plant.plant_type))
                     .where(Plant.name.startswith(plant_name))
                )

        else:
            query = Plant.select()

        format_string = "{:15} {:15}\n"

        self.text_field.config(state=tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.insert(tk.END, format_string.format('Plant Type', 'Name'))
        for plant in query:
            self.text_field.insert(tk.END, format_string.format(str(plant.plant_type.plant_type), plant.name))
        self.text_field.config(state=tk.DISABLED)
    
    @staticmethod
    def add_plant(plant_name: str, )


if __name__ == '__main__':
    root = tk.Tk()
    
    app = Application(root)
    app.mainloop()
    
    
    # print("started")
    # PlantType.create_table()
    # Plant.create_table()
    # # PlantType.create(plant_type='Дерево')
    # # Plant.create(name='Верба', plant_type=PlantType.get(PlantType.plant_type_id == 1))
    # plant = Plant.get(Plant.plant_id == 1)
    # print('plant:', plant.plant_id, plant.name, plant.plant_type)
