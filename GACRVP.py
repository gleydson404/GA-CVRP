# -*- coding: utf-8 -*-
# Representacao do invididuo deve serguir a forma:

# [custumer1, customer2, customer3, #, costumer4, costumer5, #]
# para 2 carros
# [customer1, customer2, costumer3, costumer4, #, # ]
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
from random import randint, choice
import json


# Lendo arquivo de configuracao .json
def load_parameters(file):
    with open(file) as json_file:
        parameters = json.load(json_file)
        return parameters


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_customers
def gen_ind(qtd_vehicles, qtd_customers, cstrs_list):
    # fixme vehicles vai ser gerado para cada individuo tirar
    # de dentro da funcao e passar como parametro
    vehicles = ['#' for _ in range(qtd_vehicles - 1)]
    individual = np.hstack((cstrs_list, vehicles))
    np.random.shuffle(individual)
    return individual


# Acao: Gera a populacao baseado na funcao de geracao de individuos
def gen_pop(size, qtd_vcls, qtd_cstrs, cstrs_list):
    return [gen_ind(qtd_vcls, qtd_cstrs, cstrs_list) for _ in range(size)]


# Acao: Calcula a sobrecarga por veiculo e retorna a sobrecarga do individuo
# Parametros: Individuo
# fix-me usar a função que calcula overcapacity por rota dentro dessa
def over_capacity(individual, demands, capacity):
    routes = get_routes_per_vehicle(individual)
    over = 0
    for item in routes:
        vehicle_demand = 0
        # print('veiculo')
        for inner in item:
            vehicle_demand += demands[int(inner)]
        if (capacity - vehicle_demand) < 0:
            over += capacity - vehicle_demand
    return over


# Acao: calcula o estou por rota
# parametros: assinatura da funcao é clara
def over_capacity_per_route(route, demands, capacity):
    dem = []
    for item in route:
        dem.append(demands[int(item)])

    total_demand = np.sum(dem)
    over = capacity - total_demand
    if over >= 0:
        return 0
    else:
        return over


# Acao: Calcula o fitness de um indivudo
# parametros: individuo, matriz de distancias
# fix-me @Donegas pra você não reclamar que eu mexi na sua
# funcao, eu não modifiquei ela, só coloquei o alfa
# como parametro por que eu presciso usar ele em
# outra funcao, e pra gente nao trabalhar com alfas diferente
# @Gleydson404: Brigando pelo codigo, que feio!
# Vi fundamentacao para a alteracao, nao se preocupe.
def fitness_ind(individual, dist_matrix, gama):
    # gama = melhor / (((sum(dem/cap)*cap)/2)**2) * (geracao/num_geracoes)
    custo_total = np.sum(dist_veiculo(individual, dist_matrix))
    estouro_total = np.sum(over_capacity(individual))
    fitness = custo_total + gama * estouro_total
    return fitness


# Acao: Calcula o fitness da Populacao
# Parametros: populacao
def fitness_pop(populacao, dist_matrix, gama):
    fit_pop = []
    for ind in populacao:
        fit_pop.append((fitness_ind(ind, dist_matrix, gama), ind))
    return fit_pop


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix(qtd_customers, qtd_vehicles, customers):
    dist_matrix = np.zeros((qtd_customers + 1, qtd_customers + 1))
    for i in range(qtd_customers + 1):
        for j in range(qtd_customers + 1):
            dist_matrix[i][j] = ec(customers[i], customers[j])
    return dist_matrix


# Acao: retorna uma lista com as rotas de um veiculo
# parametros:
def get_routes_per_vehicle(individual):
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


# Acao: retorna um individuo a partir de suas rotas
# Parametros: Recebe rotas e devolve individuo,
# preenchendo com # no final as rotas vazias
def get_individual_from_vehicle(routes):
    qtd_veiculos_rota = len(routes)
    dif_veiculos = qtd_vehicles - qtd_veiculos_rota - 1
    individual = []
    for i in range(len(routes)):
        individual.extend(list(routes[i]))
        individual.extend('#')
    if individual[len(individual)-1] == '#':
        del individual[-1]
    while dif_veiculos > 0:
        individual.extend('#')
        dif_veiculos = dif_veiculos - 1
    if individual.count('#') < (qtd_vehicles-1):
        individual.extend('#')
    return list(individual)


# Acao: calcula distancia da rota
# Parametros: individuo e matriz de distancias
def dist_veiculo(ind, dist_matrix, qtd_customers, qtd_vehicles):
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

def simple_one_point_cross(father, mother):
    pass


def simple_two_points_cross(father, mother):
    pass


def simple_random_cross(father, mother):
    pass


def biggest_overlap_cross(father, mother):
    pass


def horizontal_line_cross(father, mother):
    pass


# Acao: calcula o R para o crossover uniform segundo a tese de 2004
# retorna um vetor com os valores R por rota/veiculo
# parametros assinatura da funcao é bastante clara
def calc_r(ind, dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity):
    routes_cost = dist_veiculo(ind, dist_matrix, qtd_customers, qtd_vehicles)
    routes = get_routes_per_vehicle(ind)
    r_per_vehicle = []
    for i in range(len(routes)):
        fit = routes_cost[i] + gama * over_capacity_per_route(routes[i], routes[i], demands, capacity)
        r_per_vehicle.append(fit / qtd_customers)
    return r_per_vehicle


def uniform_cross(father, mother, dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity):
    child = []
    r_father = calc_r(father, dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity)
    r_mother = calc_r(mother, dist_matrix, qtd_customers, qtd_vehicles, gama,  demands, capacity)
    clone_father = father[:]
    clone_mother = mother[:]
    
    # adicionando rota de menor r ao filho
    child.append(clone_father[clone_father.index(min(r_father))])
    
    # removendo rotas da mãe que tem algum elemento da rota colocada 
    # no filho anteriormente
    dele_cl_mother = []
    for item in child:
        for inner in item:
            for inner_clone in clone_mother:
                if inner in inner_clone:
                    dele_cl_mother.append(clone_mother.index[inner_clone])                    

    for item in dele_cl_mother:
        clone_mother.remove(item)

    print clone_mother

                
# Acao: Mutacao Swap: troca genes entre 2 pontos (Tese de 2008)
# Parametros: recebe e devolve o mesmo individuo
def swap_mutation(individual):
    pontos = []
    while len(pontos) < 2:
        ponto = randint(0, len(individual)-1)
        if (individual[ponto] == "#"):
            ponto = randint(0, len(individual)-1)
        if (individual[ponto] != "#"):
            pontos.append(ponto)
    aux = individual[pontos[0]]
    individual[pontos[0]] = individual[pontos[1]]
    individual[pontos[1]] = aux
    return individual


# Acao: "Mutacao" do tipo Reversa, tese de 2004 (pag 27)
def reverse_mutation(individual):
    rotas = get_routes_per_vehicle(individual)
    veiculo = randint(0, len(rotas)-1)
    rota = rotas[veiculo]
    rota_aux = []
    for cliente in range(len(rota)):
        rota_aux.extend(rota[len(rota)-1-cliente])
    rotas[veiculo] = rota_aux
    return get_individual_from_vehicle(rotas)


# Acao: Mutacao Simples com PayOff de melhor insercao
# tese de 2004 secao 4.3.1
def simple_mutation(individual):
    # sorteia um veiculo e um cliente e o deleta
    rotas = get_routes_per_vehicle(individual)
    veiculo = randint(0, len(rotas)-1)
    cliente = choice(rotas[veiculo])
    rotas[veiculo].remove(cliente)
    # sorteia novamente um veiculo (rota) e procura pela menor distancia a
    # partir do cliente escolhido anteriormente
    veiculo = randint(0, len(rotas)-1)
    posicao = best_insertion(rotas[veiculo], int(cliente))
    rota = rotas[veiculo]
    rota.insert(posicao, cliente)
    rotas[veiculo] = rota
    return get_individual_from_vehicle(rotas)


# Acao: Dado um vetor de clientes (rota) e um cliente de partida
# retorna o cliente de menor distancia ate ele
# Parametros: uma rota e um cliente de partida,
# devolve o cliente mais perto do destino
def best_insertion(routes, client):
    vetor_dist = []
    closer = np.amax(dist_matrix)
    for index in range(len(routes)):
        rota_index = int(routes[index])
        vetor_dist.append(dist_matrix[client][rota_index])
        if vetor_dist[index] < closer:
            destino = index
    return int(destino)


# Acao: Calculo do Bounding Box por Rota
# Recebe um individuo e retorna um vetor com os 4 pontos da sua caixa
def bounding_box(individual):
    coordenadas = []
    rotas = get_routes_per_vehicle(individual)
    # pontos dos clientes por rota
    for veiculo in range(len(rotas)):
        vetor_x = []
        vetor_y = []
        rota = rotas[veiculo]
        rota.insert(0, 1)
        for cliente in rota:
            vetor_x.append(customers[int(cliente)][0])
            vetor_y.append(customers[int(cliente)][1])
        max_x, max_y = max(vetor_x), max(vetor_y)
        min_x, min_y = min(vetor_x), min(vetor_y)
        coordenadas.append([(max_x, max_y), (max_x, min_y), (min_x, min_y), (min_x, max_y)])
    return coordenadas


def evolve():
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
    customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n10-k5.vrp')
    cstrs_list = customers.keys()[1: len(customers)]
    params = load_parameters("config.json")
    pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)
    dist_matrix = gen_dist_matrix(qtd_customers, qtd_vehicles, customers)

    for i in range(params['geracoes']):
        pop = evolve()  # fixme fazer função evolve

