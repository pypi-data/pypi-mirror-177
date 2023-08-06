import numpy as np
from typing import Tuple
from multiprocessing import Pool

from EA_multiproc.Pop_multiproc import Population_multiproc
from EA_multiproc.Rec_multiproc import Rec_multiproc
from EA_multiproc.Mut_multiproc import Mutation
from EA_multiproc.Sel_multiproc import Selection


class EA_pool:
    """ Main Evolutionary Strategy class
    """
    def __init__(
        self,
        minimize: int,
        budget: int,
        patience: int,
        parents: Population_multiproc,
        offsprings: Population_multiproc,
        recombination: Rec_multiproc,
        mutation: Mutation, 
        selection: Selection,
        evaluation,
        pool_size: int,
        verbose: int,
    ):
        self.minimize = minimize
        self.budget = budget
        self.patience = patience
        self.parents = parents
        self.offspring = offsprings
        self.parents_size = parents.pop_size
        self.offspring_size = offsprings.pop_size
        self.individual_size = parents.ind_size
        self.recombination = recombination
        self.mutation = mutation
        self.selection = selection
        self.evaluation = evaluation
        self.pool_size = pool_size
        self.verbose=verbose

    def run(self) -> Tuple[np.array, np.array]:
        """ Runs the Evolutionary Strategy.
            Returns the best individual and the best fitness.
        """
        # Create processes pool
        pool = Pool(8) if self.pool_size is None else Pool(self.pool_size)
        # Initialize budget and patience
        self.curr_budget, self.curr_patience = 0, 0
        # Initialize number of better generations found and total generations counters
        self.better_generations = 0
        self.gen_count = 0
        self.all_best_evals = []
        # Initial parents evaluation
        res = pool.map(func=self.evaluation, iterable=self.parents.individuals)
        self.parents.fitnesses = np.array(res)

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
                self.recombination.curr_parents = self.parents
                res = pool.map(func=self.recombination, iterable=self.offspring.individuals)
                for ind, new_vals in zip(self.offspring.individuals, res):
                    ind.values = new_vals[0]
                    ind.mut_params = new_vals[1]

            # Mutation: mutate offspring population
            res = pool.map_async(func=self.mutation, iterable=self.offspring.individuals).get()
            for ind, new_vals in zip(self.offspring.individuals, res):
                ind.values = new_vals[0]
                ind.mut_params = new_vals[1]

            # Evaluation: evaluate offspring population
            res = pool.map(func=self.evaluation, iterable=self.offspring.individuals)
            self.offspring.fitnesses = np.array(res)

            # Selection: select the parents for the next geneation
            self.selection(self.parents, self.offspring, self.minimize)

            # Update control variables, e.g. budget and best individual
            self.update_control_vars()
        if self.verbose > 0: # prints once per run
                print(f"Best eval: {self.best_eval}")
        return self.best_indiv, np.array(self.all_best_evals)

    def population_size_control(self) -> None:
        """ Check offspring population size to match maximum budget
        """
        if (self.budget - self.curr_budget) / self.offspring_size < 1:
            new_offspring_size = self.budget - self.curr_budget
            self.offspring.pop_size = new_offspring_size
            self.offspring.individuals = self.offspring.individuals[:new_offspring_size]

    def update_control_vars(self) -> None:
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
            self.mutation.set_mut_params(self.parents)
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
        