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
from load_tests import load
import json

# Lendo arquivo de configuracao .json
with open("config.json") as json_file:
    parameters = json.load(json_file)
    # capacidade_veiculo = parameters['capacidade_veiculo']
    # print(parameters)


# clientes com suas localidades vem do arquivo de teste
# Lê arquivo de teste
clients, qtd_costumers, qtd_vehicles, capacity = load('tests/A-n10-k5.vrp')

# a demanda ja esta vindo como a terceira posicao de cada cliente, não mudei por que o sono bateu
demands = [0, 0, 19, 21, 6, 19, 7, 12, 16, 6, 16]


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
def generate_individual(qtd_vehicles, qtd_costumers):
    vehicles = ['#' for _ in range(qtd_vehicles - 1)]
    individual = np.hstack((clients.keys()[1: len(clients)], vehicles))
    np.random.shuffle(individual)
    return individual


# Acao: Calcula a sobrecarga por veiculo e retorna a sobrecarga do individuo
# Parametros: Individuo
def over_capacity(individual):
    routes = get_routes_from_vehicle(individual)
    over = 0
    for item in routes:
        vehicle_demand = 0
        # print('veiculo')
        for inner in item:
            vehicle_demand += demands[int(inner)]
        if (capacity - vehicle_demand) < 0:
            over += capacity - vehicle_demand
    return over


# Acao: Calcula o fitness de um indivudo
# parametros: individuo, matriz de distancias
def fitness_ind(individual, dist_matrix):
    gama = 1
    custo_total = np.sum(dist_veiculo(individual, dist_matrix))
    estouro_total = np.sum(over_capacity(individual))
    fitness = custo_total + gama * estouro_total
    print "fitness do individuo ", individual, " : ", fitness
    return fitness


# Acao: Calcula o fitness da Populacao
# Parametros: populacao
def fitness_pop(populacao):
	fitness_populacao = []
	for individual in populacao:
		fitness_populacao.append((fitness_ind(individual, dist_matrix), individual))
	return fitness_populacao


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
# @Donegas: Alterei o individuo para lista para não precisar mexer no codigo, nao entendi a funcao do append '#'
def get_routes_from_vehicle(individual):
    individual = list(individual)
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
# Parametros: individuo e matriz de distancias
def dist_veiculo(individual, dist_matrix):
    i = 0
    vetor_dist = []
    for x in range(qtd_vehicles):
        dist = 0
        # Verifica estouro de index, o que acontece caso a ultima rota seja 0
        if x == (qtd_vehicles - 1) and i >= len(individual):
            vetor_dist.append(0)
            return vetor_dist
        # verifica o inicio de uma nova rota e calcula a distancia do deposito ao primeiro cliente
        if (individual[i] != "#"):
            dist = dist + dist_matrix[0][int(individual[i])]
            i = i + 1
            # enquanto houver clientes nesta rota, a distancia entre eles eh somada
            while (i < len(individual) and individual[i] != "#"):
                dist = dist + dist_matrix[int(individual[i - 1])][int(individual[i])]
                i = i + 1
            # verifica o termino de uma rota e calcula a distancia entre o ultimo cliente e o deposito
            dist = dist + dist_matrix[int(individual[i - 1])][0]
        vetor_dist.append(dist)
        i = i + 1
    print vetor_dist
    return vetor_dist

# =-=-=-=-=-=-=-=-=-=-=- OPERADORES =-=-=-=-=-=-=-=-=-=-=-=-=- #

# Acao: Roleta para minimizacao
# Parametro: Populacao
def roleta(populacao):
    fitness = [individuo[0] for individuo in populacao]
    fitness_total = np.abs(np.sum(fitness))
    max_fitness = np.abs(np.max(fitness))
    min_fitness = np.abs(np.min(fitness))
    aleatorio = np.random.uniform(0, fitness_total) # gera um valor aleatorio dentro do range fitness total
    range_fitness = max_fitness + min_fitness # range entre maior e menor para usar na roleta de minimizacao
    # Minimizacao = http://stackoverflow.com/questions/8760473/roulette-wheel-selection-for-function-minimization
    for index in range(len(populacao)):
        aleatorio -= (range_fitness - fitness[index]) # o range - o fitness do individuo eh subtraido do valor aleatorio gerado ate que este seja < 0
        if aleatorio <= 0:
            return populacao[index][1]
    return populacao[len(populacao)-1][1]


# teste = generate_individual(5, 10)
# print(teste)
dist_matrix = gen_dist_matrix()
# distancia = dist_vehicle(teste, dist_matrix)
# print(distancia)
# teste = ['4',  '9',  '#',  '6',  '#',  '#',  '2',  '3',  '5',  '10',  '#', '7',  '1', '8']
individuo = ['5', '#', '7', '4', '9', '3', '6', '1', '2', '#', '8', '#', '10', '#']
print(get_routes_from_vehicle(individuo))
print(over_capacity(individuo))
# fitness_individuos = (fitness_ind(individuo, dist_matrix))
populacao = [('5', '#', '7', '4', '9', '3', '6', '1', '2', '#', '8', '#', '10', '#'),
             ('5', '#', '7', '4', '9', '3', '6', '1', '10', '#', '8', '#', '2', '#'),
             ('5', '#', '7', '4', '9', '10', '6', '1', '2', '#', '8', '#', '3', '#'),
             ('10', '#', '4', '9', '3', '6', '1', '2', '#', '8', '#', '5', '7', '#')]
fitness_populacao = (fitness_pop(populacao))
print fitness_populacao
print "Roleta: ", (roleta(fitness_populacao))
print capacity
# print(dist_matrix)
# print(crm_fit(teste, dist_matrix))
num_geracoes = parameters['capacidade_veiculo']
geracao = 1
# gama = melhor / (((sum(dem/cap)*cap)/2)**2) * (geracao/num_geracoes)
# print gama
