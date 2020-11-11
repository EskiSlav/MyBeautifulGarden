import tkinter as tk

def _delete_text_based_on_event(event):
    """function that gets called whenever entry is clicked"""
    entry = event.widget
    if entry.cget('fg') == 'grey':
       entry.delete(0, tk.END)      # delete all the text in the entry
       entry.insert(0, '')          # insert blank for user input
       entry.config(fg = 'black')
    
def _set_text_based_on_event(event, text: str):
    entry = event.widget
    if entry.get() == '':
        entry.insert(0, text)
        entry.config(fg = 'grey')

# -- Main --
def on_click(event):
    _delete_text_based_on_event(event)

def on_focusout(event):
    _set_text_based_on_event(event, 'Name')


# -- Temperature -- 
def on_temperature_entry_click(event):
    _delete_text_based_on_event(event)
       
def on_temperature_entry_min_focusout(event):
    _set_text_based_on_event(event, 'Min')

def on_temperature_entry_max_focusout(event):
    _set_text_based_on_event(event, 'Max')

def on_temperature_entry_opt_focusout(event):
    _set_text_based_on_event(event, 'Optimal')
    
# -- Watering --
def on_watering_regime_click(event):
    _delete_text_based_on_event(event)

def on_watering_regime_vol_focusout(event):
    _set_text_based_on_event(event, 'Volume(ml)')

def on_watering_regime_days_focusout(event):
    _set_text_based_on_event(event, 'Days')

def on_watering_regime_number_focusout(event):
    _set_text_based_on_event(event, 'Number')

# -- Lightning --
def on_lightning_regime_click(event):
    _delete_text_based_on_event(event)

def on_lightning_regime_focusout(event):
    _set_text_based_on_event(event, 'Level(0-5)')

# -- Flowering --

def on_flowering_period_date_click(event):
    _delete_text_based_on_event(event)

def on_flowering_period_date_focusout(event):
    _set_text_based_on_event(event, 'DD-MM')

