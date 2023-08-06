import torch
import numpy as np
from EA_torch.Population_torch import Population_torch

class Ackley_torch():
    """ Evaluate a solution on Ackley problem
        Minimization problem. Optimum is 0.
    """
    def __init__(self, a = 20, b = 0.2, c = 2*np.pi, minimize=True):
        self.a = a
        self.b = b
        self.c = c
        self.optimum = 0
        
    def __call__(self, X: Population_torch):
        ret_vals = []
        x = X.individuals
        for ind_idx in range(X.individuals.shape[0]):
            dim = x.shape[1]
            term1 = -1. * self.a * torch.exp(-1. * self.b * np.sqrt((1./dim) * sum(map(lambda i: i**2, x[ind_idx]))))
            term2 = -1. * np.exp((1./dim) * (sum(map(lambda j: torch.cos(self.c * j), x[ind_idx]))))
            y = term1 + term2 + self.a + np.exp(1)
            ret_vals.append(y)
        X.fitnesses =  torch.tensor(ret_vals)


class Bartels_torch():
    """ Evaluate a solution on Bartels problem.
        Minimization problem. Optimum is 1.
    """
    def __call__(self, X: Population_torch):
        ret_vals = []
        y = X.individuals
        for ind_idx in range(X.individuals.shape[0]):
            x = y[ind_idx]
            res = torch.sum(torch.abs(x**2 + x**2 + x*x) + torch.abs(torch.sin(x)) + torch.abs(torch.cos(x)))
            ret_vals.append(res)
        X.fitnesses =  torch.tensor(ret_vals)


class Adjiman_torch():
    """ Evaluate a solution on Adjimin problem.
        Minimization problem. Optimum is -2.02181.
    """
    def __call__(self, X: Population_torch):
        ret_vals = []
        x = X.individuals
        for ind_idx in range(X.individuals.shape[0]):
            res = torch.sum(torch.cos(x[ind_idx]) * torch.sin(x[ind_idx]) - x[ind_idx] / (x[ind_idx]**2 + 1))
            ret_vals.append(res)
        X.fitnesses =  torch.tensor(ret_vals)