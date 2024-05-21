# Menu options
OPTIONS = {
    'fm4': 'Current FM4 Song',
    'oe1liveradio': 'Current OE1 Song',
    "temperature_linz": "Temperatur in Linz",
    "temperature_bremen": "Temperatur in Bremen",
    "temperature_lissabon": "Temperatur in Lissabon"
}

# Function to determine selected option based on potentiometer value
def get_selected_option():
    adc_value = 20000
    max_value = 26404
    thresholds = [max_value / 5 * i for i in range(1, 5)]
    stations = list(OPTIONS.keys())
    for i, threshold in enumerate(thresholds):
        if adc_value < threshold:
            return stations[i]
    return stations[-1]



print(get_selected_option())