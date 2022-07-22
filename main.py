 # -*- coding: utf-8 -*-
# ---Задача---
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
import tkinter.filedialog, tkinter.messagebox
from datetime import datetime

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

        self.plant_name_label = tk.Label(self.master, text='Plant Name')
        self.plant_name_field = tk.Entry(self.master, width=25, fg='grey')
        self.plant_name_field.bind('<FocusIn>', on_click)
        self.plant_name_field.bind('<FocusOut>', on_focusout)
        self.plant_name_field.place(x=x + x_field_offset, y=y)
        self.plant_name_label.place(x=x, y=y)
        self.plant_name_field.insert(0, 'Plant Name')

        y += offset
        self.plant_type_label = tk.Label(self.master, text='Plant type')
        self.plant_type_field = tk.Entry(self.master, width=25, fg='grey')
        self.plant_type_field.bind('<FocusIn>', on_click)
        self.plant_type_field.bind('<FocusOut>', on_focusout)
        self.plant_type_field.place(x=x + x_field_offset, y=y)
        self.plant_type_label.place(x=x, y=y)
        self.plant_type_field.insert(0, 'Plant Type')

        y += offset
        self.temperature_regime_label = tk.Label(self.master, text='Temperature regime')
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
        self.watering_regime_label = tk.Label(self.master, text='Watering regime')
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
        self.lightning_regime_label = tk.Label(self.master, text='Amount of light')
        self.lightning_regime_level = tk.Entry(self.master, width=14, state=tk.NORMAL, fg='grey')
        self.lightning_regime_level.bind('<FocusIn>', on_lightning_regime_click)
        self.lightning_regime_level.bind('<FocusOut>', on_lightning_regime_focusout)
        self.lightning_regime_level.place(x=x + x_field_offset, y=y)
        self.lightning_regime_label.place(x=x, y=y)
        self.lightning_regime_level.insert(0, 'Level(0-5)')

        y += offset
        self.flowering_period_label = tk.Label(self.master, text='Flowering period')
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

        y += offset
        self.create_description_btn = tk.Button(self.master, text='Create Descripiton')
        self.create_description_btn['command'] = self.create_window
        self.create_description_btn.place(x=x, y=y)
        
        y += offset
        self.description_path_label = tk.Label(self.master, text='Heh')
        self.description_path_label.place(x=x, y=y)


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

        light_level = get_text_field(self.lightning_regime_level)

        flowering_start = get_text_field(self.flowering_period_start_date)
        flowering_end = get_text_field(self.flowering_period_end_date)
        # flowering_date_end = datetime(
        #     2000, flowering_date_end[1], flowering_date_end[0], 0, 0, 0
        #     )

        query_string = """Plant.select() \
            .join(PlantType, on=(PlantType.plant_type_id == Plant.plant_type)) \
            .join(TemperatureRegime, join_type=JOIN.LEFT_OUTER,
                  on=(TemperatureRegime.temperature_regime_id == Plant.temperature_regime)) \
            .join(WateringRegime, join_type=JOIN.LEFT_OUTER,
                  on=(WateringRegime.watering_regime_id == Plant.watering_regime)) \
            .join(LightRegime, join_type=JOIN.LEFT_OUTER,
                  on=(LightRegime.light_regime_id == Plant.light_regime)) \
            .join(FloweringPeriod, join_type=JOIN.LEFT_OUTER,
                  on=(FloweringPeriod.flowering_period_id == Plant.flowering_period))"""

        where_clause = []
        if plant_name != "":
            where_clause.append("(Plant.name.startswith(plant_name))")
        if plant_type != "":
            where_clause.append("(PlantType.plant_type.startswith(plant_type))")
        if temp_min != float('-inf'):
            where_clause.append("(TemperatureRegime.min_temperature >= temp_min)")
        if temp_max != float('inf'):
            where_clause.append("(TemperatureRegime.max_temperature <= temp_max)")
        if watering_days != '':
            where_clause.append("(WateringRegime.days == watering_days)")
        if watering_numbers != '':
            where_clause.append("(WateringRegime.number_of_times_per_days == watering_numbers)")
        if watering_vol != "":
            where_clause.append("(WateringRegime.volume == watering_vol)")
        if light_level != "":
            where_clause.append("(LightRegime.level_of_lighting == light_level)")

        

        if flowering_start != "":
            where_clause.append("""FloweringPeriod.start_flowering >= datetime(
                2000, int(flowering_start.split('-')[1]), int(flowering_start.split('-')[0]), 0, 0, 0, 0
                )""")
        if flowering_end != "":
            where_clause.append("""FloweringPeriod.end_flowering <= datetime(
            2000, int(flowering_end.split('-')[1]), int(flowering_end.split('-')[0]), 0, 0, 0, 0
            )""")


        if len(where_clause) > 0:
            query_string += ".where(" + " & ".join(where_clause) + ')'

        query = eval(query_string)
            
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
        # try:
        temp_min = get_text_field(self.temperature_regime_min)
        temp_max = get_text_field(self.temperature_regime_max)
        temp_opt = get_text_field(self.temperature_regime_opt)
        # except ValueError:
        #     tkinter.messagebox.showinfo('FYI', '!!!Wrong Data!!!')
        #     return
        volume = get_text_field(self.watering_regime_vol)
        watering_days = get_text_field(self.watering_regime_days)
        watering_number = get_text_field(self.watering_regime_numbers)
        light_level = get_text_field(self.lightning_regime_level)
        flowering_start = get_text_field(self.flowering_period_start_date)
        flowering_end = get_text_field(self.flowering_period_end_date)
        description_path = self.description_path_label['text']
        self.__add_plant(plant_name, plant_type, temp_min, temp_max, temp_opt, volume,
                         watering_days, watering_number, light_level, flowering_start,
                         flowering_end, description_path)
        tkinter.messagebox.showinfo('FYI', 'Plant Created')


    @staticmethod
    def __add_plant(plant_name: str, plant_type: str, temp_min: int=None, temp_max: int=None,
                    temp_opt: int=None, volume: int=None, watering_days: int=None, watering_number: int=None,
                    light_level: int=None, flowering_start: str=None, flowering_end: str=None,
                    description_path: str=None):
        add = True

        plant = Plant()
        
        res = list(PlantType.select().where(PlantType.plant_type == plant_type))

        if len(res) > 0:
            plant_type_model = res[0]
        else: 
            if plant_type == '':
                plant_type_model = None
            else:
                plant_type_model = PlantType()
                plant_type_model.plant_type = plant_type
                plant_type_model.save()


        res = list(TemperatureRegime.select().where(
            TemperatureRegime.optimal_temperature == temp_opt &
            TemperatureRegime.min_temperature == temp_min &
            TemperatureRegime.max_temperature == temp_max
        ))

        if len(res) > 0:
            temperature_regime = res[0]
        else:
            if temp_min == '':
                temp_min = None
            if temp_max == '':
                temp_max = None
            if temp_opt == '':
                temp_opt = None
            
            if temp_min is None and temp_max is None and temp_opt is None:
                temperature_regime = None
            else:
                temperature_regime = TemperatureRegime()
                temperature_regime.min_temperature = temp_min
                temperature_regime.max_temperature = temp_max
                temperature_regime.optimal_temperature = temp_opt
                temperature_regime.save()
        

        res = list(WateringRegime.select().where(
            WateringRegime.volume == volume &
            WateringRegime.number_of_times_per_days == watering_number &
            WateringRegime.days == watering_days
        ))

        if len(res) > 0:
            watering_regime = res[0]
        else:
            if volume == '':
                volume = None
            if watering_number == '':
                watering_number = None
            if watering_days == '':
                watering_days = None
            
            if volume is None and watering_number is None and watering_days is None:
                watering_regime = None
            else:
                watering_regime = WateringRegime()
                watering_regime.volume = volume
                watering_regime.number_of_times_per_days = watering_number
                watering_regime.days = watering_days
                watering_regime.save()
        
        if len(res) > 0:
            light_regime = res[0]
        else:
            if light_level == '':
                light_level = None
            if light_level is None:
                light_regime = None
            else:
                light_regime = LightRegime()
                light_regime.level_of_lighting = light_level
                light_regime.save()

        if len(res) > 0:
            flowering_period = res[0]
        else:
            
            flowering_period = FloweringPeriod()
            if flowering_end != '' and flowering_end != '':
                try:
                    flowering_period.start_flowering = datetime(
                        2000, int(flowering_start.split('-')[1]), int(flowering_start.split('-')[0]), 0, 0, 0, 0
                        )
                    flowering_period.end_flowering = datetime(
                        2000, int(flowering_end.split('-')[1]), int(flowering_end.split('-')[0]), 0, 0, 0, 0
                        )
                except IndexError:
                    tkinter.messagebox.showinfo('FYI', 'Wrong Flowering Date entered')
                    return
                flowering_period.save()
            else:
                flowering_period = None
            
        if description_path != '':
            plant_info = PlantInfo()
            plant_info.description_filepath = description_path
            plant_info.save()
        else:
            plant_info = None

        plant.name = plant_name
        plant.plant_type = plant_type_model
        plant.temperature_regime = temperature_regime
        plant.watering_regime = watering_regime
        plant.light_regime = light_regime
        plant.flowering_period = flowering_period
        plant.plant_info = plant_info

        plant.save()
        print('Created!\n')
     
    def create_window(self):
        self.top = tk.Toplevel(self, width=600, height=300)
        self.top.wm_title("Create Description")

        self.text_subfield = tk.Text(self.top, width=40, height=20)
        self.text_subfield.place(x=300, y=15)

        self.save_file_btn = tk.Button(self.top, text='Save to file', command=self.save_as)
        self.save_file_btn.place(x = 15, y=145)
        l = tk.Label(self.top, text="This is window")

    def save_as(self):
        filename = tkinter.filedialog.asksaveasfilename(defaultextension='.txt')
        f = open(filename, 'w')
        f.write(self.text_subfield.get('1.0', 'end'))
        f.close()
        tkinter.messagebox.showinfo('FYI', 'File Saved')
        self.description_path_label['text'] = filename
        self.top.destroy()
        self.top.update()

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
        Application.__add_plant('Клtн', 'Дерево', 1, 40, 25)
        Application.__add_plant('Дуб', 'Дерево', 5, 20, 15)
        Application.__add_plant('Граб', 'Дерево', 6, 23, 345)
        Application.__add_plant('Черешня', 'Дерево', 12, 15, 13)
        Application.__add_plant('Малина', 'Куст', 15, 23, 17)
        Application.__add_plant('Полуниця', 'Куст',12, 60, 30)

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
