 # -*- coding: utf-8 -*-


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
import peewee

from formatters import get_formatted_plant

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Application(tk.Frame):
    def __init__(self, master=None):
        
        self.WIDTH = 1000
        self.HEIGHT = 500
        self.LEFT = 300
        self.RIGHT = 300
        master.geometry("{}x{}+{}+{}".format(self.WIDTH, self.HEIGHT, self.LEFT, self.RIGHT))

        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_btn = tk.Button(self.master, text='Select')
        self.select_btn['command'] = self.select_from_db
        self.select_btn.place(x=int(self.WIDTH/8 - 30), y=int(3*self.HEIGHT/4), width=100)

        self.insert_btn = tk.Button(self.master, text='Insert')
        self.insert_btn['command'] = self.add_plant
        self.insert_btn.place(x=int(self.WIDTH/8 + 180), y=int(3*self.HEIGHT/4), width=100)
        
        self.text_field = tk.Text(self.master, width=67, height=36, state=tk.DISABLED)
        self.text_field.place(x=self.WIDTH/2 + 10, y=10) 

        offset = 25
        y = int(self.HEIGHT/4) + offset
        x = 50
        x_field_offset = 200
        subfield_offset = 50
        self.plant_name_label = tk.Label(self.master, text='Название растения')
        self.plant_name_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        self.plant_name_field.place(x=x + x_field_offset, y=y)
        self.plant_name_label.place(x=x, y=y)

        y += offset
        self.plant_type_label = tk.Label(self.master, text='Тип растения')
        self.plant_type_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        self.plant_type_field.place(x=x + x_field_offset, y=y)
        self.plant_type_label.place(x=x, y=y)

        y += offset
        self.temperature_regime_label = tk.Label(self.master, text='Температурный режим')
        self.temperature_regime_field1 = tk.Text(self.master, width=6, height=1, state=tk.NORMAL)
        self.temperature_regime_field2 = tk.Text(self.master, width=6, height=1, state=tk.NORMAL)
        self.temperature_regime_field1.place(x=x + x_field_offset, y=y)
        self.temperature_regime_field2.place(x=x + x_field_offset + subfield_offset, y=y)
        self.temperature_regime_label.place(x=x, y=y)

        y += offset
        self.watering_regime_label = tk.Label(self.master, text='Режим Полива')
        self.watering_regime_field1 = tk.Text(self.master, width=6, height=1, state=tk.NORMAL)
        self.watering_regime_field2 = tk.Text(self.master, width=6, height=1, state=tk.NORMAL)
        self.watering_regime_field1.place(x=x + x_field_offset, y=y)
        self.watering_regime_field2.place(x=x + x_field_offset + subfield_offset, y=y)
        self.watering_regime_label.place(x=x, y=y)

        y += offset
        self.lightning_regime_label = tk.Label(self.master, text='Режим Освещения')
        self.lightning_regime_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        self.lightning_regime_field.place(x=x + x_field_offset, y=y)
        self.lightning_regime_label.place(x=x, y=y)

        y += offset
        self.flowering_regime_label = tk.Label(self.master, text='Период цветения')
        self.flowering_regime_field = tk.Text(self.master, width=25, height=1, state=tk.NORMAL)
        self.flowering_regime_field.place(x=x + x_field_offset, y=y)
        self.flowering_regime_label.place(x=x, y=y)

    def select_from_db(self):
        plant_name = self.plant_name_field.get("1.0", tk.END)[:-1]
        plant_type = self.plant_type_field.get("1.0", tk.END)[:-1]

  
        query = (Plant.select()
                    .join(PlantType, on=(PlantType.plant_type_id == Plant.plant_type))
                    .where(
                        Plant.name.startswith(plant_name) and 
                        PlantType.plant_type.startswith(plant_type)
                        )
            )
        
        
        plants = query.execute()

        self.text_field.config(state=tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.insert(tk.END, "{:15} {:15}\n".format('Plant Type', 'Name'))
        for plant in plants:
            text = get_formatted_plant(plant)
            self.text_field.insert(tk.END, text)
        self.text_field.config(state=tk.DISABLED)
    
    def add_plant(self):
        plant_name = self.plant_name_field.get("1.0", tk.END)[:-1]
        plant_type = self.plant_type_field.get("1.0", tk.END)[:-1]
        self.__add_plant(plant_name, plant_type)

    @staticmethod
    def __add_plant(plant_name: str, plant_type: str):
        add = True
        while add:
            try:
                Plant.create(
                    name=plant_name, 
                    plant_type=PlantType.get(PlantType.plant_type == plant_type)
                    )
                add = False
            except peewee.DoesNotExist as e:
                print(e)
                PlantType.create(plant_type=plant_type)
    
    @staticmethod
    def _create_all_tables():
        TemperatureRegime.create_table()
        WateringRegime.create_table()
        LightRegime.create_table()
        FloweringPeriod.create_table()
        PlantInfo.create_table()
        PlantType.create_table()
        Plant.create_table()

    
    @staticmethod
    def _drop_all_tables():
        TemperatureRegime.drop_table()
        WateringRegime.drop_table()
        LightRegime.drop_table()
        FloweringPeriod.drop_table()
        PlantInfo.drop_table()
        PlantType.drop_table()
        Plant.drop_table()

    @staticmethod
    def _create_initial_rows():
        Application._delete_all_rows_in_database()
        Application.__add_plant('Клён', 'Дерево')
        Application.__add_plant('Дуб', 'Дерево')
        Application.__add_plant('Граб', 'Дерево')
        Application.__add_plant('Черешня', 'Дерево')
        Application.__add_plant('Малина', 'Куст')
        Application.__add_plant('Клубника', 'Куст')

    @staticmethod
    def _delete_all_rows_in_database():
        if input('Are you sure you want to delete all rows? (y/n): ').lower() == 'y':
            Plant.delete().where(1 == 1).execute()
            PlantType.delete().where(1 == 1).execute()



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
