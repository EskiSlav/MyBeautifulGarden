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

from formatters import *
from event_handlers import *

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def get_text_field(field: tk.Entry) -> str:
            if field.cget('fg') != 'grey':
                return field.get()
            return ""

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

        offset = 35
        y = int(self.HEIGHT/10) + offset
        x = 50
        x_field_offset = 200
        subfield_offset = 70

        self.plant_name_label = tk.Label(self.master, text='Название растения')
        self.plant_name_field = tk.Entry(self.master, width=25, fg='grey')
        self.plant_name_field.bind('<FocusIn>', on_click)
        self.plant_name_field.bind('<FocusOut>', on_focusout)
        self.plant_name_field.place(x=x + x_field_offset, y=y)
        self.plant_name_label.place(x=x, y=y)
        self.plant_name_field.insert(0, 'Plant Name')

        y += offset
        self.plant_type_label = tk.Label(self.master, text='Тип растения')
        self.plant_type_field = tk.Entry(self.master, width=25, fg='grey')
        self.plant_type_field.bind('<FocusIn>', on_click)
        self.plant_type_field.bind('<FocusOut>', on_focusout)
        self.plant_type_field.place(x=x + x_field_offset, y=y)
        self.plant_type_label.place(x=x, y=y)
        self.plant_type_field.insert(0, 'Plant Type')

        y += offset
        self.temperature_regime_label = tk.Label(self.master, text='Температурный режим')
        self.temperature_regime_min = tk.Entry(self.master, width=6, state=tk.NORMAL, fg='grey')
        self.temperature_regime_max = tk.Entry(self.master, width=6, state=tk.NORMAL, fg='grey')
        self.temperature_regime_opt = tk.Entry(self.master, width=6, state=tk.NORMAL, fg='grey')
        self.temperature_regime_min.bind('<FocusIn>', on_temperature_entry_click)
        self.temperature_regime_max.bind('<FocusIn>', on_temperature_entry_click)
        self.temperature_regime_opt.bind('<FocusIn>', on_temperature_entry_click)
        self.temperature_regime_min.bind('<FocusOut>', on_temperature_entry_min_focusout)
        self.temperature_regime_max.bind('<FocusOut>', on_temperature_entry_max_focusout)
        self.temperature_regime_opt.bind('<FocusOut>', on_temperature_entry_opt_focusout)
        self.temperature_regime_min.place(x=x + x_field_offset, y=y)
        self.temperature_regime_max.place(x=x + x_field_offset + subfield_offset, y=y)
        self.temperature_regime_opt.place(x=x + x_field_offset + subfield_offset*2, y=y)
        self.temperature_regime_label.place(x=x, y=y)
        self.temperature_regime_min.insert(0, 'Min')
        self.temperature_regime_max.insert(0, 'Max')
        self.temperature_regime_opt.insert(0, 'Optimal')


        y += offset
        self.watering_regime_label = tk.Label(self.master, text='Режим Полива')
        self.watering_regime_vol = tk.Entry(self.master, width=6, fg='grey')
        self.watering_regime_days = tk.Entry(self.master, width=6, fg='grey')
        self.watering_regime_numbers = tk.Entry(self.master, width=6, fg='grey')
        self.watering_regime_vol.place(x=x + x_field_offset, y=y)
        self.watering_regime_days.place(x=x + x_field_offset + subfield_offset, y=y)
        self.watering_regime_numbers.place(x=x + x_field_offset + subfield_offset*2, y=y)
        self.watering_regime_vol.bind('<FocusIn>', on_watering_regime_click)
        self.watering_regime_days.bind('<FocusIn>', on_watering_regime_click)
        self.watering_regime_numbers.bind('<FocusIn>', on_watering_regime_click)
        self.watering_regime_vol.bind('<FocusOut>', on_watering_regime_vol_focusout)
        self.watering_regime_days.bind('<FocusOut>', on_watering_regime_days_focusout)
        self.watering_regime_numbers.bind('<FocusOut>', on_watering_regime_number_focusout)
        self.watering_regime_label.place(x=x, y=y)
        self.watering_regime_vol.insert(0, 'Vol(ml)')
        self.watering_regime_days.insert(0, 'Days')
        self.watering_regime_numbers.insert(0, 'Number')


        y += offset
        self.lightning_regime_label = tk.Label(self.master, text='Режим Освещения')
        self.lightning_regime_level = tk.Entry(self.master, width=14, state=tk.NORMAL, fg='grey')
        self.lightning_regime_level.bind('<FocusIn>', on_lightning_regime_click)
        self.lightning_regime_level.bind('<FocusOut>', on_lightning_regime_focusout)
        self.lightning_regime_level.place(x=x + x_field_offset, y=y)
        self.lightning_regime_label.place(x=x, y=y)
        self.lightning_regime_level.insert(0, 'Level(0-5)')

        y += offset
        self.flowering_period_label = tk.Label(self.master, text='Период цветения')
        self.flowering_period_start_date = tk.Entry(self.master, width=6, fg='grey')
        self.flowering_period_end_date = tk.Entry(self.master, width=6, fg='grey')
        self.flowering_period_start_date.bind('<FocusIn>', on_flowering_period_date_click)
        self.flowering_period_end_date.bind('<FocusIn>', on_flowering_period_date_click)
        self.flowering_period_start_date.bind('<FocusOut>', on_flowering_period_date_focusout)
        self.flowering_period_end_date.bind('<FocusOut>', on_flowering_period_date_focusout)
        self.flowering_period_start_date.place(x=x + x_field_offset, y=y)
        self.flowering_period_end_date.place(x=x + x_field_offset + subfield_offset, y=y)
        self.flowering_period_label.place(x=x, y=y)
        self.flowering_period_end_date.insert(0, 'DD-MM')
        self.flowering_period_start_date.insert(0, 'DD-MM')


    def select_from_db(self):

        

        plant_name = get_text_field(self.plant_name_field)
        plant_type = get_text_field(self.plant_type_field)
        
        temp_min = get_text_field(self.temperature_regime_min)
        temp_max = get_text_field(self.temperature_regime_max)
        temp_opt = get_text_field(self.temperature_regime_opt)
        
        try:
            temp_min = int(temp_min) if temp_min != '' else float('-inf')
            temp_max = int(temp_max) if temp_max != '' else float('inf')
            temp_opt = int(temp_opt) if temp_opt != '' else 0
        except ValueError:
            temp_min, temp_max, temp_opt = float('-inf'), float('inf'), 0

        watering_vol = get_text_field(self.watering_regime_vol)
        watering_days = get_text_field(self.watering_regime_days)
        watering_numbers = get_text_field(self.watering_regime_numbers)

        query = Plant.select() \
            .join(PlantType, on=(PlantType.plant_type_id == Plant.plant_type)) \
            .join(TemperatureRegime, join_type=JOIN.LEFT_OUTER,
                  on=(TemperatureRegime.temperature_regime_id == Plant.temperature_regime)) \
            .join(WateringRegime, join_type=JOIN.LEFT_OUTER,
                  on=(WateringRegime.watering_regime_id == Plant.watering_regime)) \
            .join(LightRegime, join_type=JOIN.LEFT_OUTER,
                  on=(LightRegime.light_regime_id == Plant.light_regime)) \
            .join(FloweringPeriod, join_type=JOIN.LEFT_OUTER,
                  on=(FloweringPeriod.flowering_period_id == Plant.flowering_period)) \
            .where(
                Plant.name.startswith(plant_name) &
                PlantType.plant_type.startswith(plant_type) &
                TemperatureRegime.min_temperature >= temp_min &
                TemperatureRegime.max_temperature <= temp_max
            )
            
        plants = query.execute()

        self.text_field.config(state=tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        # self.text_field.insert(tk.END, "{:15} {:15}\n".format('Plant Type', 'Name'))
        for plant in plants:
            text = get_formatted_plant(plant)
            self.text_field.insert(tk.END, text)
        self.text_field.config(state=tk.DISABLED)
    
    def add_plant(self):
        plant_name = get_text_field(self.plant_name_field)
        plant_type = get_text_field(self.plant_type_field)
        temp_min = get_text_field(self.temperature_regime_min)
        temp_max = get_text_field(self.temperature_regime_max)
        temp_opt = get_text_field(self.temperature_regime_opt)
        self.__add_plant(plant_name, plant_type, temp_min, temp_max, temp_opt)

    @staticmethod
    def __add_plant(plant_name: str, plant_type: str, temp_min: int=None, temp_max: int=None,
                    temp_opt: int=None, volume: int=None, watering_days: int=None, watering_number: int=None,
                    light_level: int=None, flowering_start: str=None, flowering_end: str=None):
        add = True
        while add:
            try:
                Plant.create(
                    name=plant_name, 
                    plant_type=PlantType.get(PlantType.plant_type == plant_type),
                    temperature_regime=TemperatureRegime.get(
                            (TemperatureRegime.optimal_temperature == temp_opt) & 
                            (TemperatureRegime.min_temperature == temp_min) &
                            (TemperatureRegime.max_temperature == temp_max)
                        )
                    )
                add = False
            except peewee.DoesNotExist as e:
                PlantType.create(plant_type=plant_type)
                TemperatureRegime.create(optimal_temperature=temp_opt, 
                                         min_temperature=temp_min,
                                         max_temperature=temp_max)
    
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
