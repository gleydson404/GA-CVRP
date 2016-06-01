# -*- coding: utf-8 -*-
# Representacao do invididuo deve serguir a forma:

# [custumer1, costumer2, costumer3, #, costumer4, costumer5, #]
# para 2 carros
# [costumer1, costumer2, costumer3, costumer4, #, # ]
# também para 2 carros, mas nesse caso, apenas 1 carro tem rota

# Estao sendo utilizados # como separadores porque consideramos que
# todos os carros tem capacidades iguais
#
# Os parametros para a execucao geral do algoritmo
# devem vir de um arquivo conifg.json que deve
# estar na mesma pasta que este script


import numpy as np
from Distances import euclidian as ec
import json

# Lendo arquivo de configuracao .json
with open("config.json") as json_file:
    parameters = json.load(json_file)
    # capacidade_veiculo = parameters['capacidade_veiculo']
    # print(parameters)

# parametro colocado aqui enquanto não é possivel ler o
# arquivo de teste
qtd_costumers = 10
qtd_vehicles = 5
capacity = 50
# apenas preenchendo uma lista com o id de cada cliente que depois
# deve virar uma strig
costumers = [i for i in range(1, qtd_costumers + 1)]

# clientes com suas localidades vem do arquivo de teste
# Lê arquivo de teste
with open("test.json") as json_file:
    tests = json.load(json_file)
ids = [int(test) for test in tests]
clients = {}
for i in ids:
    clients[ids[i]] = tests[str(ids[i])]
# fix-me adicionei mais um 0 referente ao deposito tem que ver como vai ficar 
demands = [0, 0, 19, 21, 6, 19, 7, 12, 16, 6, 16]


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
# FIX Gerando veículos+1
def generate_individual(qtd_vehicles, qtd_costumers):
    vehicles = ['#' for _ in range(qtd_vehicles - 1)]
    individual = np.hstack((costumers, vehicles))
    np.random.shuffle(individual)
    return individual


def over_capacity(individual):
    routes = get_routes_from_vehicle(individual)
    over = 0
    for item in routes:
        vehicle_demand = 0
        print('veiculo')
        for inner in item:
            vehicle_demand += demands[int(inner)]
        if (capacity - vehicle_demand) < 0:
            over += capacity - vehicle_demand
    return over


# Acao: Calcula o fitness de um indivudo
# parametros: individuo
def crm_fit(individual, dist_matrix):
    # dist_vehicle = get_dist_vehicle(individual, get_dist_vehicle)
    # total_cost = np.sum(dist_vehicle)
    pass


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix():
    dist_matrix = np.zeros((qtd_costumers + 1, qtd_costumers + 1))
    for i in range(qtd_costumers + 1):
        for j in range(qtd_costumers + 1):
            dist_matrix[i][j] = ec(clients[i], clients[j])
    return dist_matrix


# Acao: retorna uma lista com as rotas de um veiculo
# parametros:
def get_routes_from_vehicle(individual):
    individual.append('#')
    routes = []
    elesments = []
    for i in range(len(individual)):
        if individual[i] != '#':
            elesments.append(individual[i])
        else:
            if elesments:
                routes.append(elesments[:])
                elesments[:] = []
    return routes


# Acao: calcula distancia da rota
def get_dist_vehicle(individual, dist_matrix):
    i = 0
    vetor_dist = []
    dist_matrix = gen_dist_matrix()
    for x in range(qtd_vehicles):
        dist = 0
        if x == (qtd_vehicles - 1) and i >= len(individual):
            vetor_dist.append(0)
            return vetor_dist
        if (individual[i] != "#"):
            dist = dist + dist_matrix[0][int(individual[i])]
            i = i + 1
            while (i < len(individual) and individual[i] != "#"):
                dist = dist + dist_matrix[int(individual[i - 1])][int(individual[i])]
                i = i + 1
            dist = dist + dist_matrix[int(individual[i - 1])][0]
        vetor_dist.append(dist)
        i = i + 1
    return vetor_dist


# teste = generate_individual(5, 10)
# print(teste)
# dist_matrix = gen_dist_matrix()
# distancia = dist_vehicle(teste, dist_matrix)
# print(distancia)
# teste = ['4',  '9',  '#',  '6',  '#',  '#',  '2',  '3',  '5',  '10',  '#', '7',  '1', '8']
teste = ['5', '#', '7', '4', '9', '3', '6', '1', '2', '#', '8', '#', '10', '#']
print(get_routes_from_vehicle(teste))
print(over_capacity(teste))
# print(dist_matrix)
# print(crm_fit(teste, dist_matrix))
