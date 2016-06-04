from GACRVP import *
import numpy as np
customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n10-k5.vrp')
cstrs_list = customers.keys()[1: len(customers)]
params = load_parameters("config.json")
pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)
dist_matrix = gen_dist_matrix(qtd_customers, qtd_vehicles, customers)
gama = 1
p1 = ['7', '6', '10', '1', '4', '#', '5', '#', '3', '8', '2', '#', '9', '#']
p2 = ['9', '#', '6', '7', '5', '#', '10', '1', '#', '2', '8', '3', '4', '#']

demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8]

# print(dist_veiculo(p1, dist_matrix, qtd_customers, qtd_vehicles))
# print(dist_veiculo(p2, dist_matrix, qtd_customers, qtd_vehicles))
# print customers[1]
uniform_cross(p1, p2, dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity)
