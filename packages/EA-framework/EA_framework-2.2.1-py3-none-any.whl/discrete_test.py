from EA_sequential.Population import *
from EA_sequential.Recombination import *
from EA_sequential.Mutation import *
from EA_sequential.Selection import *
from EA_sequential.Evaluation import *
from EA_sequential.EA import *
from EA_sequential.Crossover import *

ea = EA(minimize=False,budget=1000, patience=None,
    parents_size=6, individual_size=50, offspring_size=42, discrete=True, 
    recombination=GlobalDiscrete(), mutation=BitFlip(p=0.05), selection=PlusSelection(), evaluation=OneMax(),
    verbose=2)

ea.run()