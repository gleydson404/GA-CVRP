from GACRVP import *
import numpy as np
from Distances import euclidian
customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n10-k5.vrp')
cstrs_list = customers[:, 0]
params = load_parameters("config.json")
pop = gen_pop(10, qtd_vehicles, qtd_customers, cstrs_list)
dist_matrix = gen_dist_matrix(qtd_customers, customers)
gama = 1
p1 = ['7', '6', '10', '1', '4', '#', '5', '#', '3', '8', '2', '#', '9', '#']
p2 = ['9', '#', '6', '7', '5', '#', '10', '1', '#', '2', '8', '3', '4', '#']

# demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8]

print(customers)
