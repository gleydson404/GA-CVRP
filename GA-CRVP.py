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
from LoadTests import load
import json


# Lendo arquivo de configuracao .json
def load_parameters(file):
    with open(file) as json_file:
        parameters = json.load(json_file)
        return parameters


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
def gen_ind(qtd_vehicles, qtd_costumers, costumers_list):
    vehicles = ['#' for _ in range(qtd_vehicles - 1)]
    individual = np.hstack((costumers_list, vehicles))
    np.random.shuffle(individual)
    return individual


# Acao: Gera a populacao baseado na funcao de geracao de individuos
def gen_pop(size, qtd_vehicles, qtd_costumers, costumers_list):
    return [gen_ind(qtd_vehicles, qtd_costumers, costumers_list) for _ in range(size)]


# Acao: Calcula a sobrecarga por veiculo e retorna a sobrecarga do individuo
# Parametros: Individuo
def over_capacity(individual, demands, capacity):
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
    return fitness


# Acao: Calcula o fitness da Populacao
# Parametros: populacao
def fitness_pop(populacao, dist_matrix):
    fit_pop = []
    for individual in populacao:
        fit_pop.append((fitness_ind(individual, dist_matrix), individual))
    return fit_pop


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix(qtd_costumers, qtd_vehicles, costumers):
    dist_matrix = np.zeros((qtd_costumers + 1, qtd_costumers + 1))
    for i in range(qtd_costumers + 1):
        for j in range(qtd_costumers + 1):
            dist_matrix[i][j] = ec(costumers[i], costumers[j])
    return dist_matrix


# Acao: retorna uma lista com as rotas de um veiculo
# parametros:
# @Donegas: Alterei o individuo para lista para não precisar
# mexer no codigo, nao entendi a funcao do append '#'
# @gleydson404 Han?
# fix-me
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
def dist_veiculo(ind, dist_matrix, qtd_costumers, qtd_vehicles):
    i = 0
    vetor_dist = []
    for x in range(qtd_vehicles):
        dist = 0
        # Verifica estouro de index, o que acontece caso a ultima rota seja 0
        if x == (qtd_vehicles - 1) and i >= len(ind):
            vetor_dist.append(0)
            return vetor_dist
        # verifica o inicio de uma nova rota e calcula a distancia
        # do deposito ao primeiro cliente
        if (ind[i] != "#"):
            dist = dist + dist_matrix[0][int(ind[i])]
            i = i + 1
            # enquanto houver clientes nesta rota, a distancia
            # entre eles eh somada
            while (i < len(ind) and ind[i] != "#"):
                dist = dist + dist_matrix[int(ind[i - 1])][int(ind[i])]
                i = i + 1
            # verifica o termino de uma rota e calcula a distancia
            # entre o ultimo cliente e o deposito
            dist = dist + dist_matrix[int(ind[i - 1])][0]
        vetor_dist.append(dist)
        i = i + 1
    return vetor_dist

# =-=-=-=-=-=-=-=-=-=-=- OPERADORES =-=-=-=-=-=-=-=-=-=-=-=-=- #


def simple_one_poins_cross(father, mother):
    pass


def simple_two_poins_cross(father, mother):
    pass


def simple_random_cross(father, mother):
    pass


def biggest_overlap_cross(father, mother):
    pass


def horizontal_line_cross(father, mother):
    pass


def uniform_cross(father, mother):
    pass


def simple_random_mut(ind):
    pass


# Acao: Roleta para minimizacao
# Parametro: Populacao
def roleta(populacao):
    fitness = [individuo[0] for individuo in populacao]
    fitness_total = np.abs(np.sum(fitness))
    max_fitness = np.abs(np.max(fitness))
    min_fitness = np.abs(np.min(fitness))
    # gera um valor aleatorio dentro do range fitness total
    aleatorio = np.random.uniform(0, fitness_total)
    # range entre maior e menor para usar na roleta de minimizacao
    range_fitness = max_fitness + min_fitness
    # Minimizacao = http://stackoverflow.com/questions/8760473/
    # roulette-wheel-selection-for-function-minimization
    for index in range(len(populacao)):
        # o range - o fitness do individuo eh subtraido do valor
        # aleatorio gerado ate que este seja < 0
        aleatorio -= (range_fitness - fitness[index])
        if aleatorio <= 0:
            return populacao[index][1]
    return populacao[len(populacao)-1][1]


if __name__ == '__main__':
    # clientes com suas localidades vem do arquivo de teste
    # Lê arquivo de teste
    costumers, qtd_costumers, qtd_vehicles, capacity = load('tests/A-n10-k5.vrp')
    params = load_parameters("config.json")

    dist_matrix = gen_dist_matrix(qtd_costumers, qtd_vehicles, costumers)
    for i in range(params['geracoes']):
        pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_costumers, costumers.keys()[1: len(costumers)])
