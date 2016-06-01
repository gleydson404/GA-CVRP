import numpy as np


def load(file):
    clients = {}
    qtd_clients = 0
    qtd_trucks = 0
    capacity = 0
    count = 0
    cord = False
    demand = False
    f = open(str(file), 'r')
    for i in f:
        if 'COMMENT' in i:
            x = 0
            while count < 2:
                if i[x].isdigit():
                    qtd_trucks = str(qtd_trucks) + i[x]
                if i[x] == ',':
                    count += 1
                x += 1
        if 'DIMENSION' in i:
            qtd_clients = int(''.join(([x for x in i if x.isdigit()])))
        if 'CAPACITY' in i:
            capacity = int(''.join(([x for x in i if x.isdigit()])))
        if 'DEPOT_SECTION' in i:
            demand = False
            cord = False
        if demand:
            demands = i.split()
            points = np.array(clients[int(demands[0])])
            demand_point = np.array((int(demands[1])))
            points = np.hstack((points, demand_point))
            clients[int(demands[0])] = points
        if 'DEMAND_SECTION' in i:
            demand = True
            cord = False
        if cord:
            line = i.split()
            clients[int(line[0])] = (int(line[1]), int(line[2]))
        if 'NODE_COORD_SECTION ' in i:
            cord = True
    f.close()
    clients[0] = np.array([0, 0, 0])
    return clients, qtd_clients, int(qtd_trucks), capacity

# print load('tests/A-n10-k5.vrp')


