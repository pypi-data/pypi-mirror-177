from multiprocessing import Process, Pool
import numpy as np
import time

from EA_sequential.Population import Population
from EA_sequential.Recombination import Recombination, GlobalDiscrete
from EA_sequential.Mutation import Mutation, IndividualSigma
from EA_sequential.Selection import Selection, CommaSelection
from EA_sequential.Evaluation import Ackley
from EA_sequential.EA import EA

from EA_multiproc.EA_pool import EA_pool
from EA_multiproc.Pop_multiproc import Population_multiproc
from EA_multiproc.Rec_multiproc import GlobalDiscrete_multiproc
from EA_multiproc.Mut_multiproc import IndividualSigma_multiproc
from EA_multiproc.Sel_multiproc import CommaSelection_multiproc
from EA_multiproc.Eval_multiproc import Ackley_multiproc

# Global parameters
minimize = True
pop_size = 3
off_size = 21
ind_size = 21
budget = 50
discrete = False
patience = 5
verbose=0

# Sequential execution ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
m = IndividualSigma()
pop = Population(
    pop_size,
    ind_size,
    False,
    mutation=m
)
off_pop = pop = Population(
    off_size,
    ind_size,
    False,
    mutation=m,
)
rec_ = GlobalDiscrete()
sel_ = CommaSelection()
ev_ = Ackley()
ea = EA(minimize=minimize, budget=budget, patience=patience,
        parents_size=pop_size, offspring_size=off_size, individual_size=ind_size,
        discrete=discrete, recombination=rec_, mutation=m, selection=sel_, evaluation=ev_, verbose=verbose)
t_start = time.time()
best_ind, best_eval = ea.run()
t_end = time.time()
print(f"EA no parallelization time: {np.round(t_end - t_start,3)}, eval: {min(best_eval)}")


# Parallel EA execution ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pop_ind = Population_multiproc(
    pop_size=pop_size,
    ind_size=ind_size, 
    discrete=discrete,
)
off_ind = Population_multiproc(
    pop_size=off_size,
    ind_size=ind_size, 
    discrete=discrete,
)
mut = IndividualSigma_multiproc()
mut.set_mut_params(pop_ind)
mut.set_mut_params(off_ind)
rec = GlobalDiscrete_multiproc()
sel = CommaSelection_multiproc()
ev = Ackley_multiproc()
ea_pool = EA_pool(minimize=True, budget=budget, patience=patience, 
                parents=pop_ind, offsprings=off_ind,
                recombination=rec, mutation=mut, selection=sel, evaluation=ev,
                pool_size=None, verbose=verbose)


t_start = time.time()
best_ind, best_eval = ea_pool.run()
t_end = time.time()
print(f"EA parallelization time: {np.round(t_end - t_start,3)}, eval: {min(best_eval)}")
