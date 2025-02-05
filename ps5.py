# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy
import math
import ps4

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
    retval = []
    for degree in degs:
        retval.append(pylab.array(pylab.polyfit(x,y,degree))) #creating a model for each degree
    return retval


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
    tss = []
    rss = []
    mean = (sum(y)/len(y))
    for value in range(len(y)):
    #Creating total sum of squares and residual sum of squares as lists first for more transparency
        tss.append(math.pow((y[value])-(mean),2)) 
        rss.append(math.pow((estimated[value])-(y[value]),2))
    rsq = 1 - (sum(rss)/sum(tss))
    return float(rsq)



def evaluate_model_on_training(x,y,models):
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
    #xvar = refunction(x,y,models)
    #for i in range(len(models)):
    #    midlist=[]
    #    for j in range(len(models[i])):
    #        midlist.append((xvar[i][j]*models[i][j]))
    #    pred.append(sum(midlist))
    for model in models:
        polyd = pylab.poly1d((model))
        pylab.figure(len(model)-1,clear=True)
        pylab.plot(x,y,"o")
        pylab.plot(x,polyd(x),"r-")
        if len(model) == 2:
            pylab.title(('Predicted Temperature by Years',"RSQ=",r_squared(y, polyd(x)),"Degree=",len(model)-1,"SE/slope=",float(se_over_slope(x,y,polyd(x),model))))
        else:
            pylab.title(("Predicted Temperature by Years","RSQ=",r_squared(y, polyd(x)),"Degree=",len(model)-1))
        pylab.xlabel("Year")
        pylab.ylabel("Predicted Temperature")
        pylab.show()
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
    retlist=[]
    for year in range(len(years)):
        midlist = []
        for city in multi_cities:
            yeartemp = climate.get_yearly_temp(city, years[year])
            yearavg = sum(yeartemp)/len(yeartemp)
            midlist.append(yearavg)
        retlist.append(sum(midlist)/len(midlist))
    retarray = pylab.array(retlist)
    return retarray

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
    retlist=[]
    for i in range(len(y)):
        if i-window_length+1 >= 0: 
            placement = (i-window_length+1)
        else:
            placement = 0 #in case the moving average attempts to go before the first index
        if placement == i:
            retlist.append(y[i])
        else:
            value = float(sum(y[placement:(i+1)])/len(y[placement:(i+1)]))
            retlist.append(value)
    return pylab.array(retlist)

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
    rss=[]
    for value in range(len(y)):
    #Creating total sum of squares and residual sum of squares as lists first for more transparency
        rss.append(math.pow((estimated[value])-(y[value]),2))
    rmse = numpy.sqrt(sum(rss)/len(rss))
    return rmse

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
    retlist=[]
    avg =gen_cities_avg(climate, multi_cities, years)
    for year in range(len(years)):
        midlist = []
        midval = 0
        for city in multi_cities:
            yeartemp = climate.get_yearly_temp(city, years[year])
            midlist.append(yeartemp)
        midlist = sum(midlist)/len(midlist)
        for value in midlist:
            midval = midval + numpy.pow((value-float(avg[year])),2)
        retlist.append(numpy.sqrt(midval/len(midlist)))
    retarray = pylab.array(retlist)
    return retarray
                

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
    for model in models:
        polyd = pylab.poly1d((model))
        pylab.figure(len(model)-1,clear=True)
        pylab.plot(x,y,"o")
        pylab.plot(x,polyd(x),"r-")
        pylab.title(("Predicted Temperature by Years","RSQ=",r_squared(y, polyd(x)),"Degree=",len(model)-1))
        pylab.xlabel("Year")
        pylab.ylabel("Predicted Temperature")
        pylab.show()

if __name__ == '__main__':

    climate = Climate('data.csv')

    # Part A.4
    templistA = []

    #for year in TRAINING_INTERVAL:
    #    templistA.append(climate.get_daily_temp("NEW YORK", 1, 10, year))
    #coefsA = generate_models(TRAINING_INTERVAL, templistA, [1])
    #evaluate_model_on_training(pylab.array(TRAINING_INTERVAL), templistA, coefsA)
   
    #templist2A = []
    #climate = Climate('data.csv')
    #templist2A = (list(gen_cities_avg(climate, ["NEW YORK"], TRAINING_INTERVAL)))
    #coefs2A = generate_models(TRAINING_INTERVAL, templist2A, [1])
    #evaluate_model_on_training(pylab.array(TRAINING_INTERVAL), templist2A, coefs2A)
    # Part B
    templistB = []
    #climate = Climate('data.csv')
    templistB = (list(gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)))
    #coefsB = generate_models(TRAINING_INTERVAL, templistB, [1])
    #evaluate_model_on_training(pylab.array(TRAINING_INTERVAL), templistB, coefsB)

    # Part C
    #templistC=[]
    #templistC=(moving_average(templistB, 5))
    #coefsC = generate_models(TRAINING_INTERVAL, templistC, [1])
    #evaluate_model_on_training(pylab.array(TRAINING_INTERVAL), templistC, coefsC)

    # Part D.2
    #templist2D = moving_average(list(gen_cities_avg(climate, CITIES, TRAINING_INTERVAL)),5)
    #coefs2D=generate_models(TRAINING_INTERVAL,templist2D,[1,2,20])
    #print(coefs2D)
    #evaluate_model_on_training(pylab.array(TRAINING_INTERVAL), templist2D, coefs2D)
    #templist3D = moving_average(list(gen_cities_avg(climate, CITIES, TESTING_INTERVAL)),5)
    #evaluate_models_on_testing(pylab.array(TESTING_INTERVAL), templist3D, coefs2D)
    # Part E
    templistE = moving_average(list(gen_std_devs(climate, CITIES, TRAINING_INTERVAL)),5)
    coefsE=generate_models(TRAINING_INTERVAL,templistE,[1])
    evaluate_model_on_training(pylab.array(TRAINING_INTERVAL),templistE,coefsE)
