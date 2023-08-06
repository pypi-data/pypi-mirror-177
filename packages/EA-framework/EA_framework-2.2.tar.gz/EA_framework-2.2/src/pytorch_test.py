from time import time
from EA_sequential.Population import *
from EA_sequential.Recombination import *
from EA_sequential.Mutation import *
from EA_sequential.Selection import *
from EA_sequential.Evaluation import *
from EA_torch.Population_torch import *
from EA_torch.Recombination_torch import *
from EA_torch.Mutation_torch import *
from EA_torch.Selection_torch import *
from EA_torch.Evaluation_torch import *
from EA_torch.EA_torch import run_EA


def main():
    device = "cuda"

    pop_size=20
    off_size=140
    ind_size = 50000
    budget = 10000
    pat = 3

    # mut = IndividualSigma()
    # pop = Population(pop_size,ind_size, mut)
    # off = Population(off_size,ind_size, mut)
    # rec = Intermediate()
    # sel = CommaSelection()
    # eval_ = Bartels()

    mut_torch = IndividualSigma_torch(device)
    # rec_torch = Intermediate_torch()
    # rec_torch = GlobalDiscrete_torch(device)
    rec_torch = None
    sel_torch = CommaSelection_torch()
    eval_torch = Adjiman_torch()
    # eval_torch = Bartels_torch()

    pop_torch = Population_torch(pop_size,ind_size, mut_torch, device)
    off_torch = Population_torch(off_size,ind_size, mut_torch, device)


    st_t = time()
    run_EA( pop_torch, off_torch, 
            rec_torch, mut_torch, sel_torch, eval_torch,
            budget, pat, True)
    end_t = time()
    print(f"Tot time: {end_t-st_t}")



        



if __name__ == "__main__":
    main()


# pop_torch.fitnesses = torch.tensor([random.uniform(0.,1.) for _ in pop_torch.individuals])


# print(pop_torch.individuals)
# st_t = time()
# for i in range(1000):
#     eval_torch(pop_torch)
#     eval_torch(off_torch)
#     sel_torch(pop_torch, off_torch)
# end_t = time()
# print(f"Torch selection time: {end_t - st_t}")
# # print(pop_torch.individuals)

# st_t = time()
# for i in range(1000):
#     eval_(pop)
#     eval_(off)
#     sel(pop, off)
# end_t = time()
# print(f"Numpy recomb time: {end_t - st_t}")

# st_t = time()
# for i in range(1000):
#     rec_torch(pop_torch, off_torch)
# end_t = time()
# print(f"Torch recomb time: {end_t - st_t}")

# st_t = time()
# for i in range(1000):
#     rec(pop,off)
# end_t = time()
# print(f"Numpy recomb time: {end_t - st_t}")


# st_t = time()
# for i in range(1000):
#     mut_torch.mutate(pop_torch)
# end_t = time()
# print(f"Torch mutation time: {end_t - st_t}")

# st_t = time()
# for i in range(10000):
#     mut.mutate(pop)
# end_t = time()
# print(f"Individual sigma time: {end_t - st_t}")

