import numpy as np
from EA_sequential.Population import *


class Selection:
    def __call__(self):
        pass


class PlusSelection(Selection):
    """ Get the best individuals from both the parent and offspring populations
    """
    def __call__(self, parents: Population, offspring: Population, minimize=True):
        fitnesses_stacked = np.hstack([parents.fitnesses, offspring.fitnesses])
        # get sorted indexes
        if minimize:
            sorted_ind = np.argsort(fitnesses_stacked)[:parents.pop_size]
        else: 
            sorted_ind = np.argsort(fitnesses_stacked)[::-1][:parents.pop_size]
        # update parent population
        parents.individuals = np.vstack([parents.individuals, offspring.individuals])[sorted_ind]
        parents.fitnesses = fitnesses_stacked[sorted_ind] 
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            parents.mut_params = np.vstack([parents.mut_params, offspring.mut_params])[sorted_ind]


class CommaSelection(Selection):
    """ Get the best individuals only from the offspring population
    """
    def __call__(self, parents: Population, offspring: Population, minimize=True):
        # get sorted indexes
        if minimize:
            sorted_ind = np.argsort(offspring.fitnesses)[:parents.pop_size]
        else:  # we need to reverse our indexes
            sorted_ind = np.argsort(offspring.fitnesses)[::-1][:parents.pop_size]
        # update parent population
        parents.individuals = offspring.individuals[sorted_ind]
        parents.fitnesses = offspring.fitnesses[sorted_ind]
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            parents.mut_params = offspring.mut_params[sorted_ind]

