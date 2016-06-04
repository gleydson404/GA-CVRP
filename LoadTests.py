import numpy as np


def load(file):
    qtd = int(''.join(([x for x in file if x.isdigit()])[0: 2]))
    clients = np.zeros((qtd, 4), np.uint8)
    clients_temp = []
    qtd_clients = 0
    qtd_trucks = 0
    capacity = 0
    cord = False
    demand = False
    f = open(str(file), 'r')
    for i in f:
        if 'COMMENT' in i:
            line = i[i.find(',') + 1: len(i)][0: i.find(',')]
            qtd_trucks = int(''.join(([x for x in line if x.isdigit()])))
        if 'DIMENSION' in i:
            qtd_clients = int(''.join(([x for x in i if x.isdigit()])))
        if 'CAPACITY' in i:
            capacity = int(''.join(([x for x in i if x.isdigit()])))
        if 'DEPOT_SECTION' in i:
            demand = False
            cord = False
        if demand:
            demands = i.split()
            points = np.array(clients_temp[int(demands[0]) - 1])
            demand_point = np.array((int(demands[1])))
            points = np.hstack((points, demand_point))
            clients[int(demands[0]) - 1, :] = points
        if 'DEMAND_SECTION' in i:
            demand = True
            cord = False
        if cord:
            line = i.split()
            clients_temp.append([int(line[0]), int(line[1]), int(line[2])])
        if 'NODE_COORD_SECTION ' in i:
            cord = True
    f.close()
    return clients, int(qtd_clients), int(qtd_trucks), int(capacity)

# costumer, x, y, z = load('tests/A-n10-k5.vrp')
# print costumer
# print costumer[:, 3]

