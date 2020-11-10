# Основні класи: рослина (назва рослини, тип рослини, фото, посилання на файл з описом, 
# температурний режим, режим поливу, режим освітлення, період цвітіння), список рослин. 
# Основні функції: ведення списку рослин, пошук рослини за різними ознаками, ведення довідника 
# типів рослин, типів режимів поливу та освітлення. 
from typing import IO
from peewee import *

conn = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = conn

class PlantType(BaseModel):
    plant_type_id = AutoField(column_name='Id')
    plant_type = TextField(column_name='Type', null=True)
    class Meta:
        table_name = 'PlantTypes'

class Regime:
    pass

class TemperatureRegime(Regime):
    pass

class WateringRegime(Regime):
    pass

class LightRegime(Regime):
    pass

class FloweringPeriod:
    pass

class Plant(BaseModel):
    plant_id = AutoField(column_name='Id')
    name = TextField(column_name='Name', null=True) 
    plant_type = ForeignKeyField(PlantType, backref='PlantType') 
    # photo = photo 
    # description_filepath = description_filepath 
    # temperature_regime = temperature_regime 
    # watering_regime = watering_regime 
    # light_regime = light_regime 
    # flowering_period = flowering_period
    # def __init__(self, name: str, plant_type: str=None, photo: IO=None, description_filepath: str=None,
    #              temperature_regime: TemperatureRegime=None, watering_regime: WateringRegime=None,
    #              light_regime: LightRegime=None, flowering_period: FloweringPeriod=None):

    def __str__(self):
        return "{:15} {:15}\n".format(self.name, self.plant_type.plant_type)

    class Meta:
        table_name = 'Plants'

    
    
        

class ListOfPlants(list):
    pass
