from EA_sequential .Population import *
import numpy as np


class EA:
    """ Main Evolutionary Strategy class
    """
    def __init__(self, minimize, budget, patience,
                parents_size, offspring_size,
                individual_size, discrete,
                recombination, mutation, 
                selection, evaluation,
                verbose):
        self.minimize = minimize
        self.budget = budget
        self.patience = patience
        self.parents_size = parents_size
        self.offspring_size = offspring_size
        self.individual_size = individual_size
        self.discrete = discrete
        self.recombination = recombination
        self.mutation = mutation
        self.selection = selection
        self.evaluation = evaluation
        self.verbose=verbose
        self.parents = Population(  self.parents_size,
                                    self.individual_size,
                                    self.discrete, mutation)
        self.offspring = Population(self.offspring_size, 
                                    self.individual_size,
                                    self.discrete, mutation)

    def run(self):
        """ Runs the Evolutionary Strategy.
            Returns the best individual and the best fitness.
        """
        # Initialize budget and patience
        self.curr_budget, self.curr_patience = 0, 0
        # Initialize number of better generations found and total generations counters
        self.better_generations = 0
        self.gen_count = 0
        self.all_best_evals = []
        # Initial parents setup
        self.evaluation(self.parents)
        self.best_eval, self.best_index = self.parents.best_fitness(self.minimize)
        self.best_indiv = self.parents.individuals[self.best_index]
        self.curr_budget += self.parents_size

        # debug print
        if self.verbose > 1: # prints zeneration 0 best eval
            print(f"Generation {self.gen_count} Best eval: {np.round(self.best_eval, 3)}, budget: {self.curr_budget}/{self.budget}")

        while self.curr_budget < self.budget:
            # check offspring population size to match maximum budget
            self.population_size_control()
            # Recombination: creates new offspring
            if self.recombination is not None:
                self.recombination(self.parents, self.offspring)
            # Mutation: mutate offspring population
            self.mutation(self.offspring)
            # Evaluation: evaluate offspring population
            self.evaluation(self.offspring)
            # Selection: select the parents for the next geneation
            self.selection(self.parents, self.offspring, self.minimize)
            # Update control variables, e.g. budget and best individual
            self.update_control_vars()
        if self.verbose > 0: # prints once per run
                print(f"Best eval: {self.best_eval}")
        return self.best_indiv, np.array(self.all_best_evals)

    def population_size_control(self):
        """ Check offspring population size to match maximum budget
        """
        if (self.budget - self.curr_budget) / self.offspring_size < 1:
            new_offspring_size = self.budget - self.curr_budget
            self.offspring.pop_size = new_offspring_size
            self.offspring.individuals = self.offspring.individuals[:new_offspring_size]
            if self.offspring.mut_params is not None:
                self.offspring.mut_params = self.offspring.mut_params[:new_offspring_size]

    def update_control_vars(self):
        """ Updates all control variables
        """
        # Update the best individual
        # best individual is in the first position due to selection
        curr_best_eval, _ = self.parents.best_fitness(minimize=self.minimize)
        self.all_best_evals.append(curr_best_eval)

        # increment budget and generation counter
        self.curr_budget += self.offspring.pop_size
        self.gen_count += 1

        # reset sigmas if patience has been defined
        if self.patience is not None and self.curr_patience >= self.patience:
            if self.verbose > 1:
                print(f"~~ Reinitializing sigmas for generation {self.gen_count}. ~~")
            self.parents.mut_params_init()
            self.curr_patience = 0

        if (self.minimize and curr_best_eval < self.best_eval) \
            or (not self.minimize and curr_best_eval > self.best_eval):  # min or max new best conditions
            self.best_indiv = self.parents.individuals[0]
            self.best_eval = curr_best_eval
            # increment number of successful generations
            self.better_generations += 1
            # reset patience since we found a new best
            self.curr_patience = 0
            # debug print
            if self.verbose > 1: # prints every time the algorithm finds a new best
                print(f"Generation {self.gen_count} Best eval: {np.round(self.best_eval, 3)}, budget: {self.curr_budget}/{self.budget}")
        else:  # new best not found, increment current patience counter
            if self.verbose > 1:
                print(f"Generation {self.gen_count}, no new best found. Budget: {self.curr_budget}/{self.budget}")
            self.curr_patience += 1
        