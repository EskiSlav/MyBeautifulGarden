from mytypes import Plant, Regime

def get_formatted_regime(regime: Regime) -> str:
    return regime.__str__()

def get_formatted_plant(plant: Plant) -> str:
    return plant.__str__()
