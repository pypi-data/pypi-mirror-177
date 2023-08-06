import numpy as np

from EA_multiproc.Pop_multiproc import Population_multiproc
from EA_sequential.Selection import Selection 

class CommaSelection_multiproc(Selection):
    """ Get the best individuals only from the offspring population
    """
    def __call__(
        self,
        parents: Population_multiproc,
        offspring: Population_multiproc,
        minimize=True
    ) -> None:
        # get sorted indexes
        if minimize:
            sorted_ind = np.argsort(offspring.fitnesses)[:parents.pop_size]
        else:  # we need to reverse our indexes
            sorted_ind = np.argsort(offspring.fitnesses)[::-1][:parents.pop_size]
        # update parent population
        parents.individuals = [offspring.individuals[i] for i in sorted_ind]
        # parents.individuals = [offspring.individuals[i] for i in sorted_ind]
        # parents.individuals = offspring.individuals[sorted_ind]
        parents.fitnesses = offspring.fitnesses[sorted_ind]