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

#Lendo arquivo de configuracao .json
with open("config.json") as json_file:
    parameters = json.load(json_file)
    #capacidade_veiculo = parameters['capacidade_veiculo']
    #print(parameters)

# parametro colocado aqui enquanto não é possivel ler o
# arquivo de teste
qtd_costumers = 10
qtd_vehicles = 5

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


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
# FIX Gerando veículos+1
def generate_individual(qtd_vehicles, qtd_costumers):
    vehicles = ['#' for _ in range(qtd_vehicles - 1)]
    individual = np.hstack((costumers, vehicles))
    np.random.shuffle(individual)
    return individual


# Acao: Calcula o fitness de um indivudo
# parametros: individuo
# fix-me calcular direito o fitness de acordo com as sequencias de numeros 
def crm_fit(individual, dist_matrix):
    distances = []
    for i in range(1, qtd_costumers):
        if individual[i] != '#':
            if i == 0:
                distances.append(dist_matrix[0][i])
            else:
                distances.append(dist_matrix[i][i + 1])
            if i == (qtd_costumers - 1):
                distances.append(dist_matrix[i][0])

    #print(distances)


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix():
    dist_matrix = np.zeros((qtd_costumers + 1, qtd_costumers + 1))
    for i in range(qtd_costumers + 1):
        for j in range(qtd_costumers + 1):
            dist_matrix[i][j] = ec(clients[i], clients[j])
            #print dist_matrix
    #print dist_matrix
    return dist_matrix

# Acao: calcula distancia da rota
def dist_veiculo(individual):
    i = 0
    vetor_distancias = []
    dist_matrix = gen_dist_matrix()
    for x in range(qtd_vehicles):
        dist = 0
        if x == (qtd_vehicles-1) and i >= len(individual):
            vetor_distancias.append(0)
            return vetor_distancias
        if (individual[i] != "#"):
            dist = dist + dist_matrix[0][int(individual[i])]
            i = i + 1
            while (i < len(individual) and individual[i] != "#"):
                dist = dist + dist_matrix[int(individual[i-1])][int(individual[i])]
                i = i + 1
            dist = dist + dist_matrix[int(individual[i-1])][0]
        vetor_distancias.append(dist)
        i = i + 1
    return vetor_distancias


teste = generate_individual(5, 10)
print(teste)
distancia = dist_veiculo(teste)
print distancia
#dist_matrix = gen_dist_matrix()
#print(dist_matrix)
#print(crm_fit(teste, dist_matrix))
