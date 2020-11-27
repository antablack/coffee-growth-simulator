
import matplotlib.pyplot as plt
import math

INTERVALE_OF_MONTHS = 3
YEARS_TO_SIMULATE = 5


def get_months():
    months = []
    for month in range(0, (12 * YEARS_TO_SIMULATE), INTERVALE_OF_MONTHS):
        months.append(month)
    return months

def get_prediction(x): # R^2 0.997
    return 16.8 + (5.77 * x) + (-0.0367) * x**2

def year_to_months(year):
    return year * 12

def get_baseline(months):
    ideal_predictions = []
    for month in months:
        ideal_predictions.append(get_prediction(month))
    return ideal_predictions

def water_requirements(params, month):
    x = params['densidad']
    if month >= 0 and month < year_to_months(1):
        return 1.6 + (2.24 * (10**-4)) * x + (-1.02 * (10**-8)) * x**2 
    elif month >= year_to_months(1) and month < year_to_months(3):
        return -1.71 + 0.566 * math.log(x)
    elif month >= year_to_months(3):
        return 2.99 + (1.79 * (10**-4)) * x + (-5.76 * (10**-9)) * x**2
    else:
        return 0

def defficit_water(params, water_requirement):
    return params['cad'] - (water_requirement * (params['meses_cons_secos'] * 30))



def start_simulation(params, months, ideal_predictions):
    simulation = []
    for i in range(len(months)):
        month = months[i]
        prediction = ideal_predictions[i]

        

        prediction = prediction * 0.5
        simulation.append(prediction)
    
    return simulation


if __name__ == '__main__':
    
    params = {
        'densidad': 5500,
        'cad': 57,
        'meses_cons_secos': 2
    }
    print(water_requirements(params, 38))
    
    months = get_months()
    ideal_predictions = get_baseline(months)
    predictions = start_simulation(params, months, ideal_predictions)
    print(ideal_predictions)
    print('---------')
    print(predictions)
    plt.plot(months, ideal_predictions, 'o-')
    plt.plot(months, predictions, 'o-')
    plt.ylabel('Altura (cm)') 
    plt.xlabel('Tiempo (meses)')
    #plt.show()
    #get_baseline()