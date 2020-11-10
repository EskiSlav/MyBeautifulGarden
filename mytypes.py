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

    def __str__(self):
        return " {:15} ".format(self.plant_type)

    class Meta:
        table_name = 'PlantTypes'

class Regime:
    pass

class TemperatureRegime(Regime, BaseModel):
    "Temperature in Celsius"
    temperature_regime_id = AutoField(column_name='Id')
    optimal_temperature = DecimalField()
    min_temperature = DecimalField()
    max_temperature = DecimalField()
    class Meta:
        table_name = 'TemperatureRegimes'

class WateringRegime(Regime, BaseModel):
    watering_regime_id = AutoField(column_name='Id')
    volume = DecimalField()
    days = DecimalField()
    number_of_times_per_days = DecimalField()
    class Meta:
        table_name = 'WateringRegimes'

class LightRegime(Regime, BaseModel):
    """
    level of light:
    - 0: Does not need light
    - 1: low
    - 2: medium
    - 3: high
    """
    light_regime_id = AutoField(column_name='Id')
    level_of_lighting = DecimalField()
    class Meta:
        table_name = 'LightRegimes'

class FloweringPeriod(BaseModel):
    flowering_period_id = AutoField(column_name='Id')
    start_flowering = DateField()
    end_flowering = DateField()

    class Meta:
        table_name = 'FloweringPeriods'

class PlantInfo(BaseModel):
    plant_info_id = AutoField(column_name='Id')
    description_filepath = TextField(column_name='DescriptionPath', null=True)
    photo_filepath = TextField(column_name='PhotoPath', null=True)

    class Meta:
        table_name = 'PlantFileInfo'

class Plant(BaseModel):
    plant_id = AutoField(column_name='Id')
    name = TextField(column_name='Name', null=True) 
    plant_type = ForeignKeyField(PlantType, backref='PlantType', null=True) 
    plant_info = ForeignKeyField(PlantInfo, backref='PlantInfo', null=True)
    temperature_regime = ForeignKeyField(TemperatureRegime, backref='TemperatureRegime', null=True) 
    watering_regime = ForeignKeyField(WateringRegime, backref='WateringRegime', null=True) 
    light_regime = ForeignKeyField(LightRegime, backref='LightRegime', null=True) 
    flowering_period = ForeignKeyField(FloweringPeriod, backref='FloweringPeriod', null=True)


    def __str__(self):
        return "{:15} {:15}\n".format(self.name, self.plant_type.plant_type)

    class Meta:
        table_name = 'Plants'


class ListOfPlants(list):
    pass
