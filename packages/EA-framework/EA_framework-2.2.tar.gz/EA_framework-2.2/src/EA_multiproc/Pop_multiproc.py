import numpy as np
from typing import Tuple

class Individual:
    def __init__(self, size, discrete=False):
        self.size = size
        self.discrete = discrete
        # initialize individual values
        if discrete:
            self.values = np.random.randint(2, size=self.size)
        else:
            self.values = np.random.uniform(0, 1, size=self.size)
        self.mut_params = None # mutation relevant parameters


class Population_multiproc:
    def __init__(
        self,
        pop_size: int,
        ind_size: int,
        discrete: bool = False,
    ):
        self.pop_size = pop_size
        self.ind_size = ind_size
        self.individuals = [Individual(ind_size, discrete=discrete,) 
                            for _ in range(pop_size)]
        self.has_mut_params = False
        self.fitnesses = np.array([])

    def max_fitness(self) -> Tuple[float, int]:
        """ Return the maximum fitness and its index.
        """
        arg_max = np.argmax(self.fitnesses)
        return self.fitnesses[arg_max], arg_max 

    def min_fitness(self) -> Tuple[float, int]:
        """ Return the minimum fitness and its index.
        """
        arg_min = np.argmin(self.fitnesses)
        return self.fitnesses[arg_min], arg_min

    def best_fitness(self, minimize=True) -> Tuple[float, int]:
        """ Returns the best fitness and index of fittest individual.
            
            Params:
                - minimize: set to True for minimization optimization
        """
        best_arg = np.argmin(self.fitnesses) if minimize else np.argmax(self.fitnesses)
        return self.fitnesses[best_arg], best_arg