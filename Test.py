from GACRVP import *
import pprint
import numpy as np
from Distances import euclidian
customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n32-k5_1.vrp')
cstrs_list = customers[:, 0]
params = load_parameters("config.json")
pop = gen_pop(10, qtd_vehicles, qtd_customers, cstrs_list)
dist_matrix = gen_dist_matrix(qtd_customers, customers)
gama = 1
# p1 = ['7', '6', '10', '1 - falta cross 3', '4', '#', '5', '#', '3', '8', '2o', '#', '9', '#']
# p2 = ['9', '#', '6', '7', '5', '#', '10', '1 - falta cross 3', '#', '2', '8', '3', '4', '#']
# p1 = ['6', '10', '3', '#', '7', '5', '4', '9', '#', '1 - falta cross 3', '#', '8', '2', '#']
# p2 = ['5', '3', '10', '9', '2', '#', '8', '#', '6', '#', '7', '4', '#', '1 - falta cross 3']

# demands = [0, 19, 21, 6, 19, 7, 12, 16, 6, 16, 8]

# print(uniform_cross(p1, p2, dist_matrix,
                    # qtd_customers, qtd_vehicles, gama, customers[:, 3], capacity))

tst = ['21', '31', '19', '17', '13', '7', '26', '#',
       '12', '1 - falta cross 3', '16', '30', '#',
       '27', '24', '#',
       '29', '18', '8', '9', '22', '15', '10', '25', '5', '20', '#',
       '14', '28', '11', '4', '23', '3', '2', '6']

tst = ['13', '2', '17', '31', '#',
       '27', '8', '14', '18', '20', '32', '22', '#',
       '25', '15', '19', '9', '12', '5', '29', '24', '4', '3', '7', '#',
       '21', '6', '26', '11', '16', '10', '23', '30', '28', '#']

# v = []
# for i, x in enumerate(tst):
#     if x != '#':
#         v.append(str(int(x) + 1 - falta cross 3))
#     else:
#         v.append(x)

# print(v)
# size = len(v)
# pp = pprint.PrettyPrinter(indent=4)
# for i in range(len(dist_matrix)):
#     pp.pprint(dist_matrix[i])

# ind = get_routes_per_vehicle(v, size)
# print ind
# print dist_veiculo(ind, dist_matrix, qtd_customers, qtd_vehicles, size)
size = len(tst)
print(fitness_ind(tst, dist_matrix, 32,
                   5, customers[:, 3], capacity,  gama, size))
#
# p1 = ['4', '5', '7', '#', '10', '#', '#', '6', '#', '9', '1 - falta cross 3', '2', '8','3']
# p2 = ['9', '1 - falta cross 3', '7', '6', '#', '10', '2', '5', '#', '8', '4', '#', '3','#']
#
#
# print simple_mutation(v, dist_matrix, qtd_vehicles)


# print simple_random_cross(p1, p2, dist_matrix, qtd_vehicles)
# simple_one_point_cross(p1, p2)
# simple_two_points_cross(p1, p2)
# print(uniform_cross(p1, p2, dist_matrix,
#                     qtd_customers, qtd_vehicles, gama, customers[:, 3], capacity, 14))

tbis = ['25', '16', '26', '2', '14', '20', '19', '24', '1 - falta cross 3', '#', '27', '#', '21', '22', '23', '28',
        '29', '3', '5', '4', '7', '6', '9', '8', '11', '10', '13', '12', '15', '17', '32', '31',
        '30', '18', '#', '#']
#print get_routes_per_vehicle(tbis, len(tbis))
