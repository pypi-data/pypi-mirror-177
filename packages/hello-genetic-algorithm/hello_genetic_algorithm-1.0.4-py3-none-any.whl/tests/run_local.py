import pandas as pd 
from helloga.crossover import SinglePointCrossOver
from helloga.selector import LinearRankingSelector, LeadingSelector
from helloga.fitness import SumFitness, WeightedSumFitness
from helloga.environment import Environment

from copy import deepcopy

import logging, sys, os, random, re

if __name__ == '__main__' :
    from helloga.individual import BinaryIndividual
    import numpy as np
    def total_size(individual, size=np.array([])) :
        chr_arr = np.array(individual.chromosome)
        siz_arr = np.array(size)
        total = np.dot(chr_arr, siz_arr.T)
        return total 

    def total_size_lt250(individual, size=np.array([])) :
        total = total_size(individual, size)
        return total <= 250


    box_importance = [6, 5, 8, 7, 6, 9, 4, 5, 4, 9, 2, 1]
    box_weights = [20, 30, 60, 90, 50, 70, 30, 30, 70, 20, 20, 60]

    individuals = [ 
        BinaryIndividual([1,1,1,0,0,0,0,0,0,0,0,1],0,0),
        BinaryIndividual([1,0,0,0,1,0,0,0,0,0,0,1],0,0),
        BinaryIndividual([0,0,0,0,0,1,1,0,0,1,0,0],0,0),
        BinaryIndividual([0,0,1,0,0,0,0,0,1,0,0,1],0,0),
        BinaryIndividual([0,1,0,0,1,0,0,0,0,0,0,1],0,0),
    ]    

    sel = LeadingSelector(
        ratio = 0.5,
        constraints=[lambda x: total_size_lt250(x, box_weights)]
    )

    fit = WeightedSumFitness(weights = box_importance)
    xo = SinglePointCrossOver()

    env = Environment(
        individuals,
        selector=sel,
        crossover=xo, 
        fitness_func=fit,
        MAX_GENERATION=50,
        CAPACITY=100, 
        MAX_ITERATION=100,
        # log_level='debug'
        verbose=1,
    )

    env.evolute()

    print(env.species.population(), env.species.generations())