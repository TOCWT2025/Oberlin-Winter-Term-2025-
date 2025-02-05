#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:27:34 2025

@author: tabby
"""
import math
import numpy as np
import matplotlib.pyplot as pl
import random
import ps4
bacteria=[]
random.seed(50)
class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        #for now
        if birth_prob <= 1 and birth_prob >= 0:
            self.birth_prob = birth_prob
        else:
            raise Exception("Don't play with me")
        if death_prob <= 1 and birth_prob >= 0:
            self.death_prob = death_prob
        else:
            raise Exception("Don't play with me")
            
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """


    def is_killed(self):
        retval= False
        randvar = random.randint(0,100)
        if randvar <= int(self.death_prob*100):
            retval=True
        return retval
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """


    def reproduce(self, pop_density):
        randvar = random.randint(0,100) 
        if randvar <= int((self.birth_prob*(1-pop_density))*100):
            newbac = SimpleBacteria(self.birth_prob,self.death_prob)
            bacteria.append(newbac)
            newbac = None
        else:
            raise ps4.NoChildException()
        return bacteria

        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop


    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        total_pop = len(self.bacteria)
        return total_pop


    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        for buddy in bacteria:
            if SimpleBacteria.is_killed(buddy) == True:
                bacteria.remove(buddy)
        population_density = Patient.get_total_pop(self)/self.max_pop
        for buddy in bacteria:
            if Patient.get_total_pop(self) < self.max_pop:
                try:
                    SimpleBacteria.reproduce(buddy, population_density)
                except(ps4.NoChildException):
                    None
                    
        return bacteria
def my_little_helper(howmanyiwant,birth_prob,death_prob):
    for i in range(howmanyiwant):
        newbac = SimpleBacteria(birth_prob,death_prob)
        bacteria.append(newbac)
        newbac=None
    return bacteria
def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    avlist = []
    for population in populations:
        avlist.append(population[n])
    average = float(sum(avlist)/len(avlist))
    return average



def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    retlist=[]
    for i in range(num_trials):
        popchanges=[]
        bacteria = my_little_helper(num_bacteria,birth_prob,death_prob)
        thispatient = Patient(bacteria,max_pop)
        for i in range(300):
            popchanges.append(len(bacteria))
            bacteria = thispatient.update()
        retlist.append(popchanges)
        return retlist
    
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)
y = []
x =[]
for i in range(300):
    fart = float(calc_pop_avg(populations,i))
    y.append(fart)
    x.append(i)


ps4.make_one_curve_plot(x,y, "Timestamp", "Number of Bacteria", "Bacteria Population over Time")
def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    sqdis = []
    avg = calc_pop_avg(populations, t)
    for population in populations:
        sqdis.append((int(avg)-int(population[t]))^(2))
    almost = float(sum(sqdis)/len(sqdis))
    return (math.sqrt(almost))

def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    avg = calc_pop_avg(populations,t)
    width = 1.96 * (calc_pop_std(populations,t)/math.sqrt(float(len(populations))))
    return (avg,width)
#print(calc_95_ci(populations,299))

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob
        self.mut_prob = mut_prob
        if resistant == False:
            self.resistant = self.get_resistant()
        else:
            self.resistant = resistant


    def get_resistant(self):
        randnum = float(random.randint(0,100)/100)
        if randnum <= self.mut_prob:
            self.resistant = True
        else:

            self.resistant = False
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        retval= False
        randvar = float(random.randint(0,100)/100)
        if self.resistant == False:
            death_prob = self.death_prob/4
        else:
            death_prob = self.death_prob
        if randvar <= death_prob:
            retval=True
        return retval

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        randvar = float(random.randint(0,100)/100)
        if randvar <= self.birth_prob*(1-pop_density):
            if self.resistant == True:
                newbac = ResistantBacteria(self.birth_prob,self.death_prob,True,self.mut_prob)
            else:
                newmut = self.mut_prob*(1-pop_density)
                newbac = ResistantBacteria(self.birth_prob,self.death_prob,False,newmut)
        else:
            raise ps4.NoChildException()
        return newbac



class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria, max_pop)
        
        self.bacteria = bacteria
        self.max_pop = max_pop
        self.on_antibiotic = False


    def set_on_antibiotic(self):
        self.on_antibiotic = True

        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """


    def get_resist_pop(self):
        counter = 0
        for bacterium in self.bacteria:
            if bacterium.resistant == True:
                counter += 1
        return counter
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """


    def updater(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        survivors=[]
        babies = []
        for buddy in self.bacteria:
            if not ResistantBacteria.is_killed(buddy):
                if self.on_antibiotic == True:
                    if buddy.resistant == True:
                        survivors.append(buddy)
                else:
                    survivors.append(buddy)
        population_density = len(survivors)/self.max_pop
        for buddy in survivors:
            try:
                babies.append(buddy.reproduce(population_density))
            except(ps4.NoChildException):
                None
        self.bacteria = survivors + babies
        return len(self.bacteria)
                    
def my_resistant_helper(howmanyiwant,birth_prob,death_prob,resistant,mut_prob):
    bacteria = []
    for i in range(howmanyiwant):
        newbac = ResistantBacteria(birth_prob,death_prob,resistant,mut_prob)
        bacteria.append(newbac)
        newbac=None
    return bacteria
tester = my_resistant_helper(100, 0.30, 0.025,False,0.9)
    

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    retlist=[]
    restlist = []
    for i in range(num_trials):
        popchanges=[]
        resistantchanges=[]
        bacteria = my_resistant_helper(num_bacteria,birth_prob,death_prob,resistant,mut_prob)
        thispatient = TreatedPatient(bacteria,max_pop)
        for i in range(150):
            popchanges.append(thispatient.get_total_pop())
            resistantchanges.append(thispatient.get_resist_pop())
            thispatient.updater()
        thispatient.set_on_antibiotic()
        for i in range(250):
            popchanges.append(thispatient.get_total_pop())
            resistantchanges.append(thispatient.get_resist_pop())
            thispatient.updater()
        retlist.append(popchanges)
        restlist.append(resistantchanges)
    return retlist,restlist

#total_pop,resistant_pop = simulation_with_antibiotic(100,
#                                                      max_pop=1000,
#                                                      birth_prob=0.3,
#                                                      death_prob=0.2,
#                                                      resistant=False,
#                                                      mut_prob=0.8,
#                                                      num_trials=50)
y1 = []
y2 = []
rx = []
#for i in range(400):
#    rx.append(i)
#    y1.append(calc_pop_avg(total_pop,i))
#    y2.append(calc_pop_avg(resistant_pop,i))
#ps4.make_two_curve_plot(rx, y1, y2, "Total Population Change Over Time",
#                        "Resistance Population Change Over Time",
#                        "Timestep", "Num. Bacteria", "Bacteria Changes Over Time")
total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)
y1 = []
y2 = []
rx = []
for i in range(399):
    rx.append(i)
    y1.append(calc_pop_avg(total_pop,i))
    y2.append(calc_pop_avg(resistant_pop,i))
    if i == 199:
        print(calc_95_ci(total_pop, i))
        print(calc_95_ci(resistant_pop, i))

        
ps4.make_two_curve_plot(rx, y1, y2, "Total Population Change Over Time",
                        "Resistance Population Change Over Time",
                        "Timestep", "Num. Bacteria", "Bacteria Changes Over Time")