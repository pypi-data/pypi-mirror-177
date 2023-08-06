import numpy as np

from EA_multiproc.Pop_multiproc import Individual

class Ackley_multiproc():
    """ 
    To be used with the Individual and IndividualPopulation classes.
    Evaluate a solution on Ackley problem
    Minimization problem. Optimum is 0.
    """
    def __init__(self, a = 20, b = 0.2, c = 2*np.pi, minimize=True):
        self.a = a
        self.b = b
        self.c = c
        self.optimum = 0
        
    def __call__(self, X: Individual):
        # x = X.individuals
        dim = X.size
        term1 = -1. * self.a * np.exp(-1. * self.b * np.sqrt((1./dim) * sum(map(lambda i: i**2, X.values))))
        term2 = -1. * np.exp((1./dim) * (sum(map(lambda j: np.cos(self.c * j), X.values))))
        y = term1 + term2 + self.a + np.exp(1)
        return y