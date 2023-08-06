import torch
from torch.distributions import Normal, Uniform

class Population_torch:
    """ Attributes:
            - pop_size : size of population
            - ind_size : size of the individual
            - individuals: 'weights' of the individual that get tuned by the algorithm
            - fitness: defines how good the current individual is for the problem.
            - mutation : defines the mutation to be used in order to initialize parameters
            - sigmas : parameters used for the Individual Mutation
    """
    def __init__(self, pop_size, ind_size, mutation, device):
        self.device = device
        self.mutation = mutation
        self.pop_size = pop_size
        self.ind_size = ind_size
        self.pop_size_v = torch.tensor([pop_size], device=device)
        self.ind_size_v = torch.tensor([ind_size], device=device)
        self.fitnesses = torch.tensor([], device=device)
        # initialize individual values
        self.individuals = Normal(0,1).sample(sample_shape=(self.pop_size,self.ind_size)).to(device).type(torch.double)
        # initialize mutation parameters
        self.mut_params_init()

    def mut_params_init(self):
        """ Initialize sigma values depending on the mutation.
        """
        if self.mutation.__class__.__name__ == "IndividualSigma_torch":
            dist = Uniform(max(0, torch.min(self.individuals)/6), max(1e-5, torch.max(self.individuals)/6))
            self.mut_params = dist.sample(sample_shape=(self.pop_size,self.ind_size)).to(self.device).type(torch.double)
        else:
            exit("Mutation not defined in population.")

    def max_fitness(self):
        """ Return the maximum fitness and its index.
        """
        arg_max = torch.argmax(self.fitnesses, dim=0)
        return self.fitnesses[arg_max], arg_max 

    def min_fitness(self):
        """ Return the minimum fitness and its index.
        """
        arg_min = torch.argmin(self.fitnesses, dim=0)
        return self.fitnesses[arg_min], arg_min

    def best_fitness(self, minimize=True):
        """ Returns the best fitness and index of fittest individual.
            
            Params:
                - minimize: set to True for minimization optimization
        """
        if minimize:
            arg_max = torch.argmax(self.fitnesses, dim=0)
            return self.fitnesses[arg_max].item(), arg_max.item()
        else:
            arg_min = torch.argmin(self.fitnesses, dim=0)
            return self.fitnesses[arg_min].item(), arg_min.item()