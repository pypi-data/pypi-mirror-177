from typing import Any, Tuple
import numpy as np

from EA_multiproc.Pop_multiproc import Population_multiproc
from EA_sequential.Recombination import Recombination

class Rec_multiproc:
    def __init__(self) -> None:
        pass

    def __call__(self, offspring: Population_multiproc, *args: Any, **kwds: Any) -> Tuple[np.array, np.array]:
        pass


class GlobalDiscrete_multiproc(Rec_multiproc):
    """ Creates discrete recombined offsprings.
    """
    def __init__(self):
        self.curr_parents = None

    def __call__(self, offspring: Population_multiproc):
        if self.curr_parents is None:
            exit("Recombination current parents not defined")

        # random parent choice
        parent_choices = np.random.choice(range(self.curr_parents.pop_size), size=offspring.size)

        # create new offspring
        new_vals = np.array([self.curr_parents.individuals[choice].values[i] for i, choice in enumerate(parent_choices)])
        
        # recombine mutation parameters if required
        if self.curr_parents.has_mut_params:
            new_mut_params =np.array([self.curr_parents.individuals[choice].mut_params[i] for i, choice in enumerate(parent_choices)])
        else: new_mut_params = None

        return new_vals, new_mut_params