import pandas as pd 
import numpy as np
# from helloga.crossover import SinglePointCrossOver
# from helloga.selector import LinearRankingSelector, LeadingSelector
# from helloga.fitness import SumFitness, WeightedSumFitness

from environment import Environment
from individual import *
from crossover import *
from selector import *
from fitness import *

import logging 
import numpy as np
if __name__ == '__main__' :
    m = [
        [0,1,1,0,0],
        [1,0,1,1,0],
        [1,1,0,1,0],
        [0,1,1,0,1],
        [0,0,0,1,0],
    ]
    m = np.array(m)
    # Define the constraints
    def edge_ends_not_equal(individual, M) :

        x, y = np.where(M==1)

        result = True
        for xi, yi in zip(x, y) :
            result = (result and (individual[int(xi)] != individual[int(yi)]))

        return result
    # Test the constraints
    ind = IntegerIndividual([0,1,2,0,1],0,0,domain=list(range(5)))
    edge_ends_not_equal(ind, M=m)
    # Create several feasible individuals. Otherwise all of them will be excluded at selection step.
    # As this is a satisfaction problem, we can start the algorithm with unfeasible initialization points and hope they can reproduce feasible and fitness offsprings.
    individuals = [ 
        IntegerIndividual([1,1,1,1,1],0,0,domain=list(range(5))),
        IntegerIndividual([1,0,3,2,4],0,0,domain=list(range(5))),
        IntegerIndividual([3,4,1,2,1],0,0,domain=list(range(5))),
        IntegerIndividual([1,2,1,2,1],0,0,domain=list(range(5))),
        IntegerIndividual([3,3,1,2,1],0,0,domain=list(range(5))),
        IntegerIndividual([0,0,1,2,1],0,0,domain=list(range(5))),
        IntegerIndividual([0,4,3,2,1],0,0,domain=list(range(5))),
        IntegerIndividual([3,0,0,2,0],0,0,domain=list(range(5))),
    ]    

    # Define selector
    sel = LeadingSelector(
        ratio = 0.5,
        constraints = [lambda x: edge_ends_not_equal(x, m)],
        feasible_ratio = 0
    )

    # Define fitness
    fit = WeightedSumFitness(weights=[-1,-1,-1,-1,-1])

    # Define crossover operator
    xo = SinglePointCrossOver()
    # Create environment 
    env = Environment(
        individuals, # initial individuals with at least one feasible solution
        selector=sel, 
        crossover=xo, 
        fitness_func=fit,
        MAX_GENERATION=500, # stop criterion by generation(every time crossover op is called, the individual will be added 1 generation)
        CAPACITY=100, # total individuals in the environment could not exceed this number, otherwise cull the population until population is smaller than capacity.
        MAX_ITERATION=50, # stop when the algorithm iterates to max times. 
        CROSSOVER_RATIO=0.8,
        verbose=1, # show log ever step
    )
    # Run algorithm
    env.evolute()

    # Show population size and generation in the final state. 
    print(env.species.population(), env.species.generations())