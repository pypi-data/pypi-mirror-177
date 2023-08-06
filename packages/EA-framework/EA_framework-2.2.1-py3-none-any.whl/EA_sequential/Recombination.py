from EA_sequential.Population import Population
import numpy as np
import random


class Recombination:
    def __call__(self):
        pass


class Intermediate(Recombination):
    """ Creates offspring by taking the average values of the parents
    """
    def __call__(self, parents: Population, offspring: Population):
        for i in range(offspring.pop_size):
            # pick two parents at random
            p1, p2 = random.sample(range(parents.pop_size), k=2)
            # update offspring population
            offspring.individuals[i] = (parents.individuals[p1] + parents.individuals[p2]) / 2
            # recombine alphas if we are using them
            if parents.mutation.__class__.__name__ == "IndividualSigma":
                offspring.mut_params[i] = (parents.mut_params[p1] + parents.mut_params[p2]) / 2


class GlobalIntermediary(Recombination):
    """ Generates one offspring as the mean value of all the parents.
    """
    def __call__(self, parents: Population, offspring: Population):
        offspring.individuals = parents.individuals.mean(axis=0, keepdims=True)
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            offspring.mut_params = parents.mut_params.mean(axis=0)


class Discrete(Recombination):
    """ Creates discretely recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # reset offspring values
        offspring.individuals = []
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            offspring.mut_params = []
        # create rng for each element of every new individual
        elem_rng = np.random.uniform(size=(offspring.pop_size,offspring.ind_size))
        for i in range(offspring.pop_size):
            # sample parent individuals
            p1, p2 = random.sample(range(parents.pop_size), k=2)
            # create new individual
            offspring.individuals.append([par_1 if p >= .5 else par_2
                                        for par_1, par_2, p in 
                                        zip(parents.individuals[p1],
                                            parents.individuals[p2],
                                            elem_rng[i])])
            # create new sigmas
            if parents.mutation.__class__.__name__ == "IndividualSigma":
                offspring.mut_params.append([par_1 if p >= .5 else par_2
                                        for par_1, par_2, p in 
                                        zip(parents.mut_params[p1],
                                            parents.mut_params[p2],
                                            elem_rng[i])])
        # revert back to numpy
        offspring.individuals = np.array(offspring.individuals)
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            offspring.mut_params = np.array(offspring.mut_params)


class GlobalDiscrete(Recombination):
    """ Creates discrete recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # rng
        parent_choices = np.random.choice(range(parents.pop_size), size=(offspring.pop_size, offspring.ind_size))
        # reset offspring
        offspring.individuals = []
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            offspring.mut_params = []
        for i in range(offspring.pop_size):
            # create new offspring
            offspring.individuals.append([curr_par[curr_choice] 
                                            for curr_par, curr_choice in 
                                            zip(parents.individuals.T, 
                                                parent_choices[i])])
            
            # recombine sigmas if required
            if parents.mutation.__class__.__name__ == "IndividualSigma":
                offspring.mut_params.append([curr_par[curr_choice] 
                                                for curr_par, curr_choice in 
                                                zip(parents.mut_params.T, 
                                                    parent_choices[i])])
        # revert arrays to numpy
        offspring.individuals = np.array(offspring.individuals)
        if parents.mutation.__class__.__name__ == "IndividualSigma":
            offspring.mut_params = np.array(offspring.mut_params)
