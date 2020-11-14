# Основні класи: рослина (назва рослини, тип рослини, фото, посилання на файл з описом, 
# температурний режим, режим поливу, режим освітлення, період цвітіння), список рослин. 
# Основні функції: ведення списку рослин, пошук рослини за різними ознаками, ведення довідника 
# типів рослин, типів режимів поливу та освітлення. 
from typing import IO
from peewee import *

conn = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    def __str__(self):
        return ""
    class Meta:
        database = conn

class PlantType(BaseModel):
    plant_type_id = AutoField(column_name='Id')
    plant_type = TextField(column_name='Type', null=True)

    def __str__(self):
        return "{:15}\n".format(self.plant_type)

    class Meta:
        table_name = 'PlantTypes'

class Regime:
    def __str__(self):
        return "Regime"

class TemperatureRegime(Regime, BaseModel):
    "Temperature in Celsius"
    temperature_regime_id = AutoField(column_name='Id')
    optimal_temperature = DecimalField(column_name='optimal_temperature')
    min_temperature = DecimalField(column_name='min_temperature')
    max_temperature = DecimalField(column_name='max_temperature')

    def __str__(self):
        return super(Regime, self).__str__() + "Temperature Min:{} Max:{} Opt:{}\n".format(
            self.min_temperature, self.max_temperature, self.optimal_temperature
        )

    class Meta:
        table_name = 'TemperatureRegimes'

class WateringRegime(Regime, BaseModel):
    watering_regime_id = AutoField(column_name='Id')
    volume = DecimalField(column_name='volume')
    days = DecimalField(column_name='days')
    number_of_times_per_days = DecimalField(column_name='numbers')

    def __str__(self):
        return super(Regime, self).__str__() + "Watering {}ml {}/{}\n".format(
            self.volume, self.number_of_times_per_days, self.days
        )
        
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
    level_of_lighting = DecimalField(column_name='level')

    def __str__(self):
        return super(Regime, self).__str__() + "Light level {}\n".format(
            self.level_of_lighting
        )

    class Meta:
        table_name = 'LightRegimes'

class FloweringPeriod(BaseModel):
    flowering_period_id = AutoField(column_name='Id')
    start_flowering = DateField(column_name='start_date')
    end_flowering = DateField(column_name='end_date')

    def __str__(self):
        s = ""
        if self.start_flowering != '' and not self.start_flowering is None:
            s += "  Start Flowering: {} \n".format(str(self.start_flowering)[5:])
        if self.end_flowering != '' and not self.end_flowering is None:
            s += "  End Flowering: {}\n".format(str(self.end_flowering)[5:])
        return s


    class Meta:
        table_name = 'FloweringPeriods'

class PlantInfo(BaseModel):
    plant_info_id = AutoField(column_name='Id')
    description_filepath = TextField(column_name='DescriptionPath', null=True)
    photo_filepath = TextField(column_name='PhotoPath', null=True)

    def __str__(self):
        s = ""
        if not self.description_filepath is None:
            s += "FilePath: {}\n".format(self.description_filepath)
        if not self.photo_filepath is None:
            s += "PhotoPath: {}\n".format(self.photo_filepath)
        return s
        
            



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
        s = ""
        
        def if_not_none_add_str(arg):
            if not arg is None:
                return str(arg)
            return "" 

        s += if_not_none_add_str(self.plant_type)
        s += if_not_none_add_str(self.plant_info) 
        s += if_not_none_add_str(self.temperature_regime)
        s += if_not_none_add_str(self.watering_regime) 
        s += if_not_none_add_str(self.watering_regime)
        s += if_not_none_add_str(self.light_regime)
        s += if_not_none_add_str(self.flowering_period)
        return "- - -\n{:15}\n".format(self.name) + s

    class Meta:
        table_name = 'Plants'


class ListOfPlants(list):
    pass
