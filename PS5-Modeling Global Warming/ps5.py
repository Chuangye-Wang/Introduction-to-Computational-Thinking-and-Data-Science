# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy as np
import matplotlib.pyplot as plt
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    if type(degs) != list:
        raise ValueError('degs is not a list')
    model = []
    for deg in degs:
        model0 = np.polyfit(x, y, deg)
        model.append(model0)
    return model


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    assert len(y) == len(estimated)
    y_mean = sum(y)/len(y)
    R = 1 - sum((y - estimated)**2)/sum((y - y_mean)**2)

    return R
    
def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    degs = []
    Rs = []
    
    for model in models:
        deg = len(model) - 1
        degs.append(deg)
        parameters = np.poly1d(model)
        y_estimated = parameters(x)
        R = r_squared(y, y_estimated)
        Rs.append(R)
        plt.figure()   
        plt.plot(x, y, 'b.', x, y_estimated, 'b')
        plt.xlabel('years')
        plt.ylabel('temperature/$\degree$C')
        if deg == 1:
            SE_linear = se_over_slope(x, y, y_estimated, model)
            plt.title('deg={0}, R-square={1:.6f}, SE/slope={2:.6f}'.format(deg, R, SE_linear))
        else:
            plt.title('deg={0}, R-square={1:.6f}'.format(deg, R))

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    cities_years_temps = []
    for year in years:
        years_temps = []
        for city in multi_cities:
            temp = sum(climate.get_yearly_temp(city, year))/len(climate.get_yearly_temp(city, year))
            years_temps.append(temp)
        average_year_temp = sum(years_temps)/len(years_temps)
        cities_years_temps.append(average_year_temp)

    cities_years_temps = np.array(cities_years_temps)
    
    return cities_years_temps

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    y_average = []
    y_len = len(y)
    for i in range(0, window_length - 1):
        y_average.append(sum(y[0:i+1])/(i+1))
    for j in range(0, y_len - window_length + 1):
        y_average.append(sum(y[j: j+window_length])/window_length)
        
    return np.array(y_average)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    assert len(y) == len(estimated)
    
    return np.sqrt(sum((y - estimated)**2) / len(y))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    cities_years_temps = []
    for year in years:
        years_temps = []
        for city in multi_cities:
            temp = climate.get_yearly_temp(city, year)
            years_temps.append(temp)
        average_daily_temps = sum(years_temps)/len(years_temps)
        average_year_temp = sum(average_daily_temps)/len(average_daily_temps)
        year_std = np.sqrt(sum((np.array(average_daily_temps) - average_year_temp)**2) / len(average_daily_temps))
        cities_years_temps.append(year_std)
    
    cities_years_temps = np.array(cities_years_temps)
    
    return cities_years_temps

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    degs = []
    Rmses = []
    
    for model in models:
        deg = len(model) - 1
        degs.append(deg)
        parameters = np.poly1d(model)
        y_estimated = parameters(x)
        Rmse = rmse(y, y_estimated)
        Rmses.append(Rmse)
        plt.figure()   
        plt.plot(x, y, 'b.', x, y_estimated, 'b')
        plt.xlabel('years')
        plt.ylabel('temperature/$\degree$C')
        plt.title('deg={0}, RMSE={1:.6f}'.format(deg, Rmse))

if __name__ == '__main__':

    climate_data = Climate('data.csv')
    window_len = 5
    
    # Part A.4    
    city0 = 'NEW YORK'
    month0 = 1
    day0 = 10
    years_temp = np.ones(len(TRAINING_INTERVAL))
    i = 0
    for year in TRAINING_INTERVAL:
        years_temp[i] = climate_data.get_daily_temp(city0, month0, day0, year)
        i += 1
    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), years_temp, [1])
    evaluate_models_on_training(np.array(TRAINING_INTERVAL), years_temp, model_deg1)
    
    ave_years_temps_Newyork = gen_cities_avg(climate_data, [city0], TRAINING_INTERVAL)
#    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), ave_years_temps_Newyork, [1])
#    evaluate_models_on_training(np.array(TRAINING_INTERVAL), ave_years_temps_Newyork, model_deg1)
    
    moving_ave_Newyork = moving_average(ave_years_temps_Newyork, window_len)
    model_deg1_2_20 = generate_models(np.array(TRAINING_INTERVAL), ave_years_temps_Newyork, [1, 2, 20])
    evaluate_models_on_training(np.array(TRAINING_INTERVAL), ave_years_temps_Newyork, model_deg1_2_20)
    
    test_ave_years_temps = gen_cities_avg(climate_data, [city0], TESTING_INTERVAL)
    test_moving_ave_temps = moving_average(test_ave_years_temps, window_len)
    evaluate_models_on_testing(np.array(TESTING_INTERVAL), test_moving_ave_temps, model_deg1_2_20)
##%%    
#    # Part B
#    ave_years_temps = gen_cities_avg(climate_data, CITIES, TRAINING_INTERVAL)
#    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), ave_years_temps, [1])
#    evaluate_models_on_training(np.array(TRAINING_INTERVAL), ave_years_temps, model_deg1)
#    
#    
#    # Part C
#    moving_ave_years_temps = moving_average(ave_years_temps, window_len)
#    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), moving_ave_years_temps, [1])
#    evaluate_models_on_training(np.array(TRAINING_INTERVAL), moving_ave_years_temps, model_deg1)
#    
#    
#    # Part D.2
#    # I
#    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), moving_ave_years_temps, [1, 2, 20])
#    evaluate_models_on_training(np.array(TRAINING_INTERVAL), moving_ave_years_temps, model_deg1)
#    #II
#    test_ave_years_temps = gen_cities_avg(climate_data, CITIES, TESTING_INTERVAL)
#    test_moving_ave_temps = moving_average(test_ave_years_temps, window_len)
#    evaluate_models_on_testing(np.array(TESTING_INTERVAL), test_moving_ave_temps, model_deg1)
#    
#    
#    # Part E
#    ave_years_temps = gen_std_devs(climate_data, CITIES, TRAINING_INTERVAL)
#    moving_ave_years_temps = moving_average(ave_years_temps, window_len)
#    model_deg1 = generate_models(np.array(TRAINING_INTERVAL), moving_ave_years_temps, [1])
#    evaluate_models_on_training(np.array(TRAINING_INTERVAL), moving_ave_years_temps, model_deg1)
#    plt.ylabel('standard deviation')
