
import matplotlib.pyplot as plt
import math
import numpy as np

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

def estimate_coef(x, y): 
    # number of observations/points 
    n = np.size(x) 
  
    # mean of x and y vector 
    m_x, m_y = np.mean(x), np.mean(y) 
  
    # calculating cross-deviation and deviation about x 
    SS_xy = np.sum(y*x) - n*m_y*m_x 
    SS_xx = np.sum(x*x) - n*m_x*m_x 
  
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
  
    return (b_0, b_1) 

def nutrients_by_months(mo, month):
    if mo <= 8:
        nitrogeno = 5.55 + (0.664 * month) + (-4.46 * (10**-3)) * month**2
        urea = 12.1 + 1.43 * month + (-8.93 * (10**-3)) * month**2
        return (nitrogeno, urea)
    elif  mo > 8:
        nitrogeno = 3.95 + 0.486 * month + (4.46 * (10**-3)) * month**2
        urea = 1.25 * month + 7.5
        return (nitrogeno, urea)
    else:
        return (0, 0)

def run_linear(a, b, month): #Y= a + bX
    return a + b * month

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

    def increase_values(self, i, percentage):
         for i in range(i, len(self.predictions)):
                self.predictions[i] += self.predictions[i] * percentage
    
    def decrease_values(self, i, percentage):
         for i in range(i, len(self.predictions)):
                self.predictions[i] -= self.predictions[i] * percentage

    def apply_nutrients_restrictions(self):
 
        x_n = np.array([2, 6, 10, 14, 18]) 
        y_n = np.array([self.params['nit_2'], self.params['nit_6'], self.params['nit_10'], self.params['nit_14'], self.params['nit_18']]) 

        x_u = np.array([2, 6, 10, 14, 18]) 
        y_u = np.array([self.params['urea_2'], self.params['urea_6'], self.params['urea_10'], self.params['urea_14'], self.params['urea_18']]) 

        nitrogeno = estimate_coef(x_n, y_n) 
        urea = estimate_coef(x_u, y_u)

        for i in range(0, len(self.predictions)):
            month = self.months[i] 
            (ideal_nit, ideal_ur) = nutrients_by_months(self.params['mo'], month)
            current_nit = run_linear(nitrogeno[0], nitrogeno[1], month)
            current_ur = run_linear(urea[0], urea[1], month)


            if current_nit > ideal_nit or current_ur > ideal_ur:
                self.increase_values(i, 0.02)
            else:
                self.decrease_values(i, 0.025)

    def start(self):
        
        self.apply_water_restrictions()
        self.apply_density_restrictions()
        self.apply_nutrients_restrictions()

        return self.predictions

if __name__ == '__main__':
    params = {
        'densidad': 7500,
        'cad': 57,
        'meses_cons_secos': 1,
        'horas_brillo_solar': 1400,
        'mo': 8,
        'nit_2': 7,
        'nit_6': 9,
        'nit_10': 12,
        'nit_14': 14,
        'nit_18': 16,

        'urea_2': 15,
        'urea_6': 20,
        'urea_10': 26,
        'urea_14': 30,
        'urea_18': 35
    }
    simulation = Simulation(params)

    predictions = simulation.start()

    plt.plot(simulation.months, simulation.baseline_predictions) #, 'o-')
    plt.plot(simulation.months, predictions) #, 'o-')
    plt.ylabel('Altura (cm)') 
    plt.xlabel('Tiempo (meses)')
    plt.show()