import torch
from torch import exp
from math import sqrt
from torch.distributions import Normal
from EA_torch.Population_torch import Population_torch


class IndividualSigma_torch():
    """ Individual sigma method.
    """
    def __init__(self, device):
        self.device = device
        self.tau = torch.tensor([0.]).to(device)
        self.tau_prime = torch.tensor([0.]).to(device)

    def __call__(self, *args):
        self.mutate(*args)
    
    def mutate(self, population: Population_torch):
        # define tau and tau'
        self.tau[0] = 1 / sqrt(2*(sqrt(population.ind_size)))
        self.tau_prime[0] = 1 / sqrt(2*population.ind_size)
        # create N and N' matrixes
        normal_matr = Normal(0,self.tau).sample((population.pop_size, population.ind_size)).squeeze()
        normal_matr_prime = Normal(0,self.tau_prime).sample((population.pop_size_v))
        #update our sigmas
        population.mut_params = population.mut_params * exp(normal_matr+normal_matr_prime)
        # update our individuals
        if (population.mut_params <= 0).any(): # make sure sigmas are positive
            population.mut_params_init()
        # create noise and update population
        noises = Normal(0,population.mut_params).sample()
        population.individuals += noises


