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
# devem vir de um arquivo parameters.json que deve
# estar na mesma pasta que este script


import numpy as np
from Distances import euclidian as ec
import json

#Lendo arquivo de configuracao .json
with open("parameters.json") as json_file:
    parameters = json.load(json_file)
    capacidade_veiculo = parameters['capacidade_veiculo']
    print(capacidade_veiculo)
#    json1_data = json.loads(json1_str)[0]
# parametro colocado aqui enquanto não é possivel ler o
# arquivo de teste
qtd_costumers = 10

# apenas preenchendo uma lista com o id de cada cliente que depois
# deve virar uma strig
costumers = [i for i in range(1, qtd_costumers + 1)]

# clientes com suas localidades vem do arquivo de teste
clients = {0: [0, 0],
           1: [82, 76],
           2: [96, 44],
           3: [50, 5],
           4: [49, 8],
           5: [13, 7],
           6: [29, 89],
           7: [58, 30],
           8: [84, 39],
           9: [14, 24],
           10: [2,  39]}


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
def generate_individual(qtd_vehicles, qtd_costumers):
    vehicles = ['#' for _ in range(qtd_vehicles)]
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

    print(distances)


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix():
    dist_matrix = np.zeros((qtd_costumers + 1, qtd_costumers + 1))
    for i in range(qtd_costumers + 1):
        for j in range(qtd_costumers + 1):
            dist_matrix[i][j] = ec(clients[i], clients[j])
    return dist_matrix


teste = generate_individual(5, 10)
print(teste)
dist_matrix = gen_dist_matrix()
print(dist_matrix)
print(crm_fit(teste, dist_matrix))
