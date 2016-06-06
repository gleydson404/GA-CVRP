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
from random import randint, choice, random
import gc
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
    vehicles = ['#' for _ in xrange(qtd_vehicles - 1)]
    individual = np.hstack((cstrs_list, vehicles))
    np.random.shuffle(individual)
    return individual


# Acao: Gera a populacao baseado na funcao de geracao de individuos
def gen_pop(size, qtd_vcls, qtd_cstrs, cstrs_list):
    return np.array([gen_ind(qtd_vcls, qtd_cstrs, cstrs_list) for _ in xrange(size)])


# Acao: Calcula a sobrecarga por veiculo e retorna a sobrecarga do individuo
# Parametros: Individuo
# fix-me usar a função que calcula overcapacity por rota dentro dessa
def over_capacity(individual, demands, capacity, size_individual):
    routes = get_routes_per_vehicle(individual, size_individual)
    over = 0
    for item in routes:
        vehicle_demand = 0
        # print('rota', item)
        for inner in item:
            vehicle_demand += demands[int(inner)-1]
        if (capacity - vehicle_demand) < 0:
            over += np.abs(capacity - vehicle_demand)
    return over


# Acao: calcula o estou por rota
# parametros: assinatura da funcao é clara
def over_capacity_per_route(route, demands, capacity):
    total_demand = 0
    for i in route:
        total_demand += demands[int(i) - 1]
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
def fitness_ind(individual, dist_matrix, qtd_customers,
                qtd_vehicles, demands, capacity,  gama, size_ind):
    # gama = melhor / (((sum(dem/cap)*cap)/2)**2) * (geracao/num_geracoes)
    routes_ind = get_routes_per_vehicle(individual, size_ind)
    custo_total = np.sum(dist_veiculo(routes_ind, dist_matrix,
                         qtd_customers, qtd_vehicles, size_ind))
    estouro_total = over_capacity(individual, demands, capacity, size_ind)
    return custo_total + gama * estouro_total


# Acao: Calcula o fitness da Populacao
# Parametros: populacao
def fitness_pop(populacao, dist_matrix, qtd_customers,
                qtd_vehicles, demands, capacity, gama, size_ind):
    return [fitness_ind(ind, dist_matrix,
                        qtd_customers, qtd_vehicles, demands,
                        capacity, gama, size_ind) for ind in populacao]


# Acao: Gerar a matriz de distancias para não precisar calcular a distancia
# para um cliente todas as vezes
def gen_dist_matrix(qtd_customers, customers):
    dist_matrix = np.zeros((qtd_customers, qtd_customers))
    coord = customers[:, 1:3]
    for i in xrange(qtd_customers):
        for j in xrange(qtd_customers):
            dist_matrix[i][j] = (np.linalg.norm(coord[i] - coord[j]))/10
    return dist_matrix


# Acao: retorna uma lista com as rotas de um veiculo
# parametros:
def get_routes_per_vehicle(individual, size_individual):
    individual = list(individual)
    individual.append('#')
    # np.append(individual, '#')
    routes = []
    elesments = []
    for i in xrange(size_individual):
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
def get_individual_from_vehicle(routes, qtd_vehicles):
    qtd_veiculos_rota = len(routes)
    dif_veiculos = qtd_vehicles - qtd_veiculos_rota - 1
    individual = []
    for i in xrange(qtd_veiculos_rota):
        individual.extend(routes[i])
        individual.extend('#')
    if individual[-1] == '#':
        del individual[-1]
    while dif_veiculos > 0:
        individual.extend('#')
        dif_veiculos = dif_veiculos - 1
    if individual.count('#') < (qtd_vehicles-1):
        individual.extend('#')
    return list(individual)


# Acao: calcula distancia da rota
# Parametros: individuo e matriz de distancias
# def dist_veiculo(ind, dist_matrix, qtd_customers, qtd_vehicles):
#     i = 0
#     vetor_dist = []
#     for x in range(qtd_vehicles):
#         dist = 0
#         # Verifica estouro de index, o que acontece caso a ultima rota seja 0
#         if x == (qtd_vehicles - 1) and i >= len(ind):
#             vetor_dist.append(0)
#             return vetor_dist
#         # verifica o inicio de uma nova rota e calcula a distancia
#         # do deposito ao primeiro cliente
#         if (ind[i] != "#"):
#             dist = dist + dist_matrix[0][int(ind[i])]
#             i = i + 1
#             # enquanto houver clientes nesta rota, a distancia
#             # entre eles eh somada
#             while (i < len(ind) and ind[i] != "#"):
#                 dist = dist + dist_matrix[int(ind[i - 1])][int(ind[i])]
#                 i = i + 1
#             # verifica o termino de uma rota e calcula a distancia
#             # entre o ultimo cliente e o deposito
#         dist = dist + dist_matrix[int(ind[i - 1])][0]
#         vetor_dist.append(dist)
#         i = i + 1
#     return vetor_dist


def dist_veiculo(routes_ind, dist_matrix, qtd_customers,
                 qtd_vehicles, size_individual):
    costs = []
    # print(ind)
    # routes_ind = get_routes_per_vehicle(ind, size_individual)
    # print('individuo', ind)
    for item in routes_ind:
        cost_route = dist_matrix[0][int(item[0]) - 1]
        cost_route += dist_matrix[int(item[-1]) - 1][0]
        for i in range(len(item) - 1):
            cost_route += dist_matrix[int(item[i]) - 1][int(item[i + 1]) - 1]
        # print('custo rota', item)
        # print('custo', cost_route)
        costs.append(cost_route)
    return costs


# =-=-=-=-=-=-=-=-=-=-=- OPERADORES =-=-=-=-=-=-=-=-=-=-=-=-=- #

def simple_one_point_cross(father, mother):
    point = randint(0, len(father)-1)
    child_1 = father[0: point]
    child_1.extend(mother[point: len(mother)])
    child_2 = mother[0: point]
    child_2.extend(father[point: len(father)])
    return child_1, child_2


def simple_two_points_cross(father, mother):
    point_1 = randint(1, len(father) - 1)
    point_2 = randint(1, len(father) - 1)
    f_slice = [father[0: point_1], father[point_1: point_2], father[point_2: len(father)]]
    m_slice = [mother[0: point_1], mother[point_1: point_2], mother[point_2: len(mother)]]
    child_1 = f_slice[0]
    child_1.extend(m_slice[1])
    child_1.extend(f_slice[2])
    child_2 = m_slice[0]
    child_2.extend(f_slice[1])
    child_2.extend(m_slice[2])
    return child_1, child_2


def simple_random_cross(father, mother, dist_matrix, qtd_vehicles):
    offspring = father
    mother_subroutes = get_routes_per_vehicle(mother, len(mother))
    subroute = mother_subroutes[randint(0, len(mother_subroutes)-1)]
    for i in range(len(subroute)):
        offspring.remove(subroute[i])
    offspring_subroutes = get_routes_per_vehicle(offspring, len(offspring))
    for i in range(len(subroute)):
        sub_off_index = int(randint(0, len(offspring_subroutes)-1))
        off_subroute = offspring_subroutes[sub_off_index]
        offspring_subroutes.pop(sub_off_index)
        best_ind = best_insertion(off_subroute, subroute[i], dist_matrix)
        off_subroute.insert(best_ind, subroute[i])
        offspring_subroutes.insert(sub_off_index, off_subroute)
    return get_individual_from_vehicle(offspring_subroutes, qtd_vehicles)


def biggest_overlap_cross(father, mother):
    pass


def horizontal_line_cross(father, mother):
    pass


# Acao: calcula o R para o crossover uniform segundo a tese de 2004
# retorna um vetor com os valores R por rota/veiculo
# parametros assinatura da funcao é bastante clara
def calc_r(routes, routes_cost, gama, demands, capacity, qtd_customers):
    r_per_vehicle = []
    size_routes = len(routes)
    for i in xrange(size_routes):
        fit = (routes_cost[i] + gama *
               over_capacity_per_route(routes[i], demands, capacity))
        r_per_vehicle.append(fit / qtd_customers)
    return r_per_vehicle


def uniform_cross(father, mother, dist_matrix,
                  qtd_customers, qtd_vehicles, gama, demands,
                  capacity, size_ind):
    child = []
    routes_father = get_routes_per_vehicle(father, size_ind)
    routes_mother = get_routes_per_vehicle(mother, size_ind)
    route_cost_father = dist_veiculo(routes_father, dist_matrix,
                                     qtd_customers, qtd_vehicles, size_ind)
    route_cost_mother = dist_veiculo(routes_mother, dist_matrix,
                                     qtd_customers, qtd_vehicles, size_ind)
    r_father = calc_r(routes_father, route_cost_father,
                      gama, demands, capacity, qtd_customers)
    r_mother = calc_r(routes_mother, route_cost_mother,
                      gama, demands, capacity, qtd_customers)

    while (routes_father or routes_mother):
        # adicionando a rota de menor r de p1 no filho
        if r_father:
            child.append(routes_father.pop(r_father.index(min(r_father))))
            del r_father[r_father.index(min(r_father))]
            # removendo rotas da mãe que tem algum elemento da rota colocada
            # no filho anteriormente
            for item in child[-1]:
                for index, inner_route in enumerate(routes_mother):
                    if item in inner_route:
                        del routes_mother[index]
                        del r_mother[index]

        # adicionando a rota de menor r de p2 no filho
        if r_mother:
            # print('querotiraroindexmae', r_mother.index(min(r_mother)))
            child.append(routes_mother.pop(r_mother.index(min(r_mother))))
            del r_mother[r_mother.index(min(r_mother))]

            # removendo as rotas do pai que tem cliente em conflito
            # com a mae
            for item in child[-1]:
                for index, inner_route in enumerate(routes_father):
                    if item in inner_route:
                        del routes_father[index]
                        del r_father[index]
    
    tmp_child = np.array(child)
    tmp_child = np.hstack(tmp_child.flat)
    lefting_customers = set(father) - set(tmp_child)
    lefting_customers = list(lefting_customers)
    lefting_customers.remove('#')
    child.append(lefting_customers)
    return get_individual_from_vehicle(child, qtd_vehicles)


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
    for cliente in xrange(len(rota)):
        rota_aux.extend(rota[len(rota)-1-cliente])
    rotas[veiculo] = rota_aux
    return get_individual_from_vehicle(rotas)


# Acao: Mutacao Simples com PayOff de melhor insercao
# tese de 2004 secao 4.3.1
def simple_mutation(individual, dist_matrix, qtd_vehicles):
    # sorteia um veiculo e um cliente e o deleta
    rotas = get_routes_per_vehicle(individual, len(individual))
    veiculo = randint(0, len(rotas)-1)
    cliente = choice(rotas[veiculo])
    rotas[veiculo].remove(cliente)
    # sorteia novamente um veiculo (rota) e procura pela menor distancia a
    # partir do cliente escolhido anteriormente
    veiculo = randint(0, len(rotas)-1)
    posicao = best_insertion(rotas[veiculo], int(cliente), dist_matrix)
    rota = rotas[veiculo]
    rota.insert(posicao, cliente)
    rotas[veiculo] = rota
    return get_individual_from_vehicle(rotas, qtd_vehicles)


# Acao: Dado um vetor de clientes (rota) e um cliente de partida
# retorna o cliente de menor distancia ate ele
# Parametros: uma rota e um cliente de partida,
# devolve o cliente mais perto do destino
def best_insertion(routes, client, dist_matrix):
    vetor_dist = []
    destino = 0
    closer = np.amax(dist_matrix)
    for index in xrange(len(routes)):
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
    for veiculo in xrange(len(rotas)):
        vetor_x = []
        vetor_y = []
        rota = rotas[veiculo]
        rota.insert(0, 1)
        for cliente in rota:
            vetor_x.append(customers[int(cliente)][0])
            vetor_y.append(customers[int(cliente)][1])
        max_x, max_y = max(vetor_x), max(vetor_y)
        min_x, min_y = min(vetor_x), min(vetor_y)
        coordenadas.append([(max_x, max_y), (max_x, min_y),
                            (min_x, min_y), (min_x, max_y)])
    return coordenadas


def elitims(tx_elitims, pop, size_pop):
    qtd = int((tx_elitims * size_pop) / 100)
    # 0 no lamba por que o fitness, é o primeiro elemento de um item
    # de pop
    pop = sorted(pop, key=lambda x: x[0])

    return pop[:qtd]


def evolve(pop, params, dist_matrix, qtd_customers,
           qtd_vehicles, demands, capacity, gama, size_ind):
    new_pop = []
    fit_pop1 = fitness_pop(pop, dist_matrix, qtd_customers,
                           qtd_vehicles, demands, capacity, gama, size_ind)
    max_fitness = max(fit_pop1)
    min_fitness = min(fit_pop1)
    total_fitness = sum(fit_pop1)
    # new_pop.extend(elitims(params['taxa_elitismo'], pop))
    # print('ramanhopop', params['tamanho_pop'])
    count = 0
    while count < 100:
        index_p1 = roleta(pop, fit_pop1, max_fitness,
                          min_fitness, total_fitness)
        index_p2 = roleta(pop, fit_pop1, max_fitness,
                          min_fitness, total_fitness)
        father = pop[index_p1]
        mother = pop[index_p2]
        child = uniform_cross(father, mother, dist_matrix, qtd_customers,
                              qtd_vehicles, gama, demands, capacity, size_ind)
        # if params['taxa_mutacao'] > random():
            # child = simple_mutation(child)
        new_pop.append(child)
        count += 1
    return new_pop

# Acao: Roleta para minimizacao
# Parametro: Populacao
def roleta(populacao, fitness, max_fitness, min_fitness, fitness_total):
    # fitness = [individuo[0] for individuo in populacao]
    # fitness_total = np.abs(np.sum(fitness))
    # max_fitness = np.abs(np.max(fitness))
    # min_fitness = np.abs(np.min(fitness))
    # gera um valor aleatorio dentro do range fitness total
    aleatorio = np.random.uniform(0, fitness_total)
    # range entre maior e menor para usar na roleta de minimizacao
    range_fitness = max_fitness + min_fitness
    # Minimizacao = http://stackoverflow.com/questions/8760473/
    # roulette-wheel-selection-for-function-minimization
    size_pop = len(populacao)
    for index in xrange(size_pop):
        # o range - o fitness do individuo eh subtraido do valor
        # aleatorio gerado ate que este seja < 0
        aleatorio -= (range_fitness - fitness[index])
        if aleatorio <= 0:
            return index
    return size_pop - 1


def main():
    # clientes com suas localidades vem do arquivo de teste
    # Lê arquivo de teste
    customers, qtd_customers, qtd_vehicles, capacity =\
            load('tests/A-n32-k5.vrp')
    cstrs_list = customers[:, 0]
    params = load_parameters("config.json")
    gama = 1
    pop = gen_pop(params['tamanho_pop'], qtd_vehicles,
                  qtd_customers, cstrs_list)
    dist_matrix = gen_dist_matrix(qtd_customers, customers)
    fit_history = []
    geracoes = params['geracoes']
    demands = customers[:, 3]
    size_ind = len(pop[0])
    for i in xrange(1000):
        pop = evolve(pop, params, dist_matrix, qtd_customers,
                     qtd_vehicles, demands, capacity, gama, size_ind)
        # fit_history.append(min(pop))
        # if i % 100 == 0:
            # print("########### geracao", i)
    # print(pop[pop.index(fit_history[-1])])


if __name__ == '__main__':
    main()
