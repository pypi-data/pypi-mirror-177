from EA_torch.Population_torch import Population_torch
from EA_sequential.Recombination import Recombination
import torch
from random import sample
import numpy as np


class Intermediate_torch(Recombination):
    """ Creates offspring by taking the average values of the parents
    """
    def __call__(self, parents: Population_torch, offspring: Population_torch):
        for i in range(offspring.pop_size):
            # pick two parents at random
            p1, p2 = sample(range(parents.pop_size), k=2)
            # update offspring population
            offspring.individuals[i] = (parents.individuals[p1] + parents.individuals[p2]) / 2
            # recombine alphas if we are using them
            if parents.mutation.__class__.__name__ == "IndividualSigma_torch":
                offspring.mut_params[i] = (parents.mut_params[p1] + parents.mut_params[p2]) / 2


class GlobalDiscrete_torch(Recombination):
    """ Creates discrete recombined offsprings.
    """
    def __init__(self, device):
        self.device = device

    def __call__(self, parents: Population_torch, offspring: Population_torch):
        # rng
        parent_choices = torch.randint(0,parents.pop_size, 
                            size=(offspring.pop_size, offspring.ind_size), 
                            device=self.device)
        # print(parent_choices.shape)
        # exit()
        # reset offspring
        new_inds = []
        new_mut_params = []
        for i in range(offspring.pop_size):
            # create new offspring
            new_inds.append(torch.hstack([curr_par[curr_choice]
                                            for curr_par, curr_choice in 
                                            zip(parents.individuals.T, 
                                                parent_choices[i])]))
            # create offspring's sigmas
            new_mut_params.append(torch.hstack([curr_par[curr_choice]
                                            for curr_par, curr_choice in 
                                            zip(parents.mut_params.T, 
                                                parent_choices[i])]))

        offspring.individuals = torch.vstack(new_inds)
        offspring.mut_params = torch.vstack(new_mut_params)


class test_GlobalDiscrete_torch(Recombination):
    """ Creates discrete recombined offsprings.
    """
    def __init__(self, device):
        self.device = device

    def __call__(self, parents: Population_torch, offspring: Population_torch):
        # rng
        parent_choices = torch.randint(0,parents.pop_size, 
                            size=(offspring.pop_size, offspring.ind_size), 
                            device=self.device)
        # print(parent_choices.shape)
        # exit()
        # reset offspring
        for i, curr_off, curr_sig in zip(range(offspring.pop_size), 
                                        offspring.individuals,
                                        offspring.mut_params):
            for j, curr_par, curr_sigma, curr_choice in zip(range(offspring.ind_size),
                                                parents.individuals.T,
                                                parents.mut_params.T,
                                                parent_choices[i]):
                
                curr_off[j] = curr_par[curr_choice]
                curr_sig[j] = curr_sigma[curr_choice]