
import matplotlib.pyplot as plt
import math

INTERVALE_OF_MONTHS = 3
YEARS_TO_SIMULATE = 5

PERCENTAGE_REDUCTION_WATER_DEFICIT = 0.05
PERCENTAGE_REDUCTION_OVERDENSITY = 0.60



def get_months():
    months = []
    for month in range(0, (12 * YEARS_TO_SIMULATE)): # INTERVALE_OF_MONTHS):
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

def water_requirements(densidad, month):
    x = densidad
    if month >= 0 and month < year_to_months(1):
        return 1.6 + (2.24 * (10**-4)) * x + (-1.02 * (10**-8)) * x**2 
    elif month >= year_to_months(1) and month < year_to_months(3):
        return -1.71 + 0.566 * math.log(x)
    elif month >= year_to_months(3):
        return 2.99 + (1.79 * (10**-4)) * x + (-5.76 * (10**-9)) * x**2
    else:
        return 0

def get_optimal_density(solar_ligth_year, capacity_save_water, months_sequia):
    return 7429.170455 + (-2.160113636 * solar_ligth_year) + (39.48238636 * capacity_save_water) + (-0.08522727271 * months_sequia)

class Simulation:

    def __init__(self, params):
        self.params = params
        self.months = get_months()
        self.baseline_predictions = get_baseline(self.months)
        self.predictions = self.baseline_predictions.copy()


    def apply_water_restrictions(self):
        for month in range(0, len(self.months), 12):
            months_water_restrictions = int(self.params["meses_cons_secos"])
            cad = int(self.params['cad'])

            for i in range(months_water_restrictions):
                next_month = month + i
                water_requirement = water_requirements(params['densidad'], next_month ) * 30
                cad -= water_requirement
                if cad < 0 :
                    reduction = self.predictions[next_month] * PERCENTAGE_REDUCTION_WATER_DEFICIT
                    self.predictions[next_month] -= reduction
                    for i2 in range(next_month + 1, len(self.predictions)):
                        self.predictions[i2] -= reduction

    def apply_density_restrictions(self):
        optimal_density = get_optimal_density(self.params['horas_brillo_solar'], self.params['cad'], self.params['meses_cons_secos'])
        print(optimal_density)
        if self.params['densidad'] > optimal_density :
            over_flow = self.params['densidad'] - optimal_density
            percentage_reduction = ((over_flow * 100) / optimal_density) / 100
            for i in range(0, len(self.predictions)):
                self.predictions[i] -= self.predictions[i] * percentage_reduction * PERCENTAGE_REDUCTION_OVERDENSITY



    def start(self):
        
        self.apply_water_restrictions()
        self.apply_density_restrictions()

        return self.predictions





if __name__ == '__main__':
    params = {
        'densidad': 7500,
        'cad': 57,
        'meses_cons_secos': 1,
        'horas_brillo_solar': 1400
    }
    print(water_requirements(params['densidad'], 38))
    
    simulation = Simulation(params)

    predictions = simulation.start()

    plt.plot(simulation.months, simulation.baseline_predictions) #, 'o-')
    plt.plot(simulation.months, predictions) #, 'o-')
    plt.ylabel('Altura (cm)') 
    plt.xlabel('Tiempo (meses)')
    plt.show()
    #get_baseline()