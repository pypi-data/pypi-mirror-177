import numpy as np
from EA_torch.Population_torch import Population_torch

def run_EA( pop: Population_torch, off_pop: Population_torch, 
            rec, mut, sel, eval_, 
            budget, patience, minimize,
            verbose=2):

    curr_budget, curr_gen, better_gens , curr_pat = 0, 0, 0, 0

    # initial evaluation
    eval_(pop)
    best_eval, best_idx = pop.best_fitness(minimize)
    best_indiv = pop.individuals[best_idx]
    curr_budget += pop.pop_size
    all_best_evals = [best_eval]

    # debug print
    if verbose > 1: # prints zeneration 0 best eval
        print(f"Gen: {curr_gen} new best: {np.round(best_eval, 3)}, budget: {curr_budget}/{budget}")

    while curr_budget < budget:
        # create and evaluate new generation
        if rec is not None:
            rec(pop, off_pop)
        mut(off_pop)
        eval_(off_pop)
        sel(pop, off_pop)
        curr_gen += 1

        # budget control
        curr_budget += off_pop.pop_size
        if (budget - curr_budget) / off_pop.pop_size < 1:
            new_pop_size = budget - curr_budget
            off_pop.pop_size = new_pop_size
            off_pop.pop_size_v[0] = new_pop_size
            off_pop.individuals = off_pop.individuals[:new_pop_size]
            off_pop.mut_params = off_pop.mut_params[:new_pop_size]

        # check for new best
        curr_best, _ = pop.best_fitness(minimize)
        if (minimize and curr_best < best_eval) \
            or (not minimize and curr_best > best_eval):
            best_eval = curr_best
            best_indiv = pop.individuals[0]
            better_gens += 1
            curr_pat = 0
            print(f"Gen: {curr_gen}, new best: {np.round(best_eval, 3)}, budget: {curr_budget}/{budget}")

        else:
            print(f"Gen: {curr_gen}, no new best found.")
            curr_pat += 1
            if patience is not None and curr_pat >= patience:
                print("Resetting mutation params, patience expired.")
                pop.mut_params_init()

        all_best_evals.append(best_eval)

    print(f"Best eval found: {np.round(best_eval, 3)}")
    return best_indiv, best_eval
