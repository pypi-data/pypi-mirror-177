import torch
from EA_torch.Population_torch import Population_torch


class PlusSelection_torch():
    """ Get the best individuals from both the parent and offspring populations
    """
    def __call__(self, parents: Population_torch, offspring: Population_torch, minimize=True):
        fitnesses_stacked = torch.hstack([parents.fitnesses, offspring.fitnesses])
        # get sorted indexes
        if minimize:
            sorted_ind = torch.argsort(fitnesses_stacked)[:parents.pop_size]
        else: 
            sorted_ind = torch.argsort(fitnesses_stacked)[::-1][:parents.pop_size]
        # update parent population
        parents.individuals = torch.vstack([parents.individuals, offspring.individuals])[sorted_ind]
        parents.fitnesses = fitnesses_stacked[sorted_ind] 
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            parents.mut_params = torch.vstack([parents.mut_params, offspring.mut_params])[sorted_ind]


class CommaSelection_torch():
    """ Get the best individuals only from the offspring population
    """
    def __call__(self, parents: Population_torch, offspring: Population_torch, minimize=True):
        # get sorted indexes
        if minimize:
            sorted_ind = torch.argsort(offspring.fitnesses)[:parents.pop_size]
        else:  # we need to reverse our indexes
            sorted_ind = torch.argsort(offspring.fitnesses)[::-1][:parents.pop_size]
        # update parent population
        parents.individuals = offspring.individuals[sorted_ind]
        parents.fitnesses = offspring.fitnesses[sorted_ind]
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            parents.mut_params = offspring.mut_params[sorted_ind]