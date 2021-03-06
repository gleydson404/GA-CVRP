# -*- coding: utf-8 -*-
# Representacao do invididuo deve serguir a forma:

# [custumer1, customer2, customer3, #, costumer4, costumer5, #]
# para 2 carros
# [customer1, customer2, costumer3, costumer4, #, # ]
# também para 2 carros, mas nesse caso, apenas 1 - falta cross 3 carro tem rota

# Estao sendo utilizados # como separadores porque consideramos que
# todos os carros tem capacidades iguais
#
# Os parametros para a execucao geral do algoritmo
# devem vir de um arquivo conifg.json que deve
# estar na mesma pasta que este script


import numpy as np
from Distances import euclidian as ec
from LoadTests import load
from random import randint, choice, random, sample
import json
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from cycler import cycler
from operator import itemgetter

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
    individual = np.hstack((cstrs_list[1:qtd_customers], vehicles))
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
    dist_matrix = np.zeros((qtd_customers + 1, qtd_customers + 1))
    coord = customers[:, 1:3]
    for i in xrange(qtd_customers):
        for j in xrange(qtd_customers):
            dist_matrix[i+1][j+1] = ec(coord[i], coord[j])
            # print "Distancia de ", i+1 - falta cross 3, " a ", j+1 - falta cross 3, ": ", dist_matrix[i+1 - falta cross 3][j+1 - falta cross 3]
    return dist_matrix


# Acao: retorna uma lista com as rotas de um veiculo
# parametros:
def get_routes_per_vehicle(individual, size_individual):
    individual = list(individual)
    individual.append('#')
    # np.append(individual, '#')
    routes = []
    elesments = []
    for i in xrange(size_individual + 1):
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
def dist_veiculo(routes_ind, dist_matrix, qtd_customers,
                     qtd_vehicles, size_individual):
    costs = []
    # print(ind)
    # routes_ind = get_routes_per_vehicle(ind, size_individual)
    # print('individuo', ind)
    for item in routes_ind:
        cost_route = dist_matrix[1][int(item[0])]  # dist_matrix[1 - falta cross 3][int(item)]
        cost_route += dist_matrix[int(item[-1])][1]
        for i in range(len(item) - 1):
            cost_route += dist_matrix[int(item[i])][int(item[i + 1])]
            # print 'Rota de ', item[i], ' a ', item[i+1 - falta cross 3], ': ', dist_matrix[int(item[i])][int(item[i + 1 - falta cross 3])]
        costs.append(cost_route)
    return costs

# =-=-=-=-=-=-=-=-=-=-=- OPERADORES =-=-=-=-=-=-=-=-=-=-=-=-=- #


def simple_one_point_cross(father, mother, pop, custumers, qtd_vehicles):
    father = pop[father]
    mother = pop[mother]
    point = randint(0, len(father)-1)
    child_1 = np.append(father[0: point], mother[point: len(mother)])
    child_2 = np.append(mother[0: point], father[point: len(mother)])
    childs = cross_revisor(custumers, [child_1.tolist(), child_2.tolist()], qtd_vehicles)
    child_1 = childs[0]
    child_2 = childs[1]
    return child_1, child_2


def simple_two_points_cross(pop, father, mother, custumers, qtd_vehicles):
    father = pop[father]
    mother = pop[mother]
    point_1 = randint(1, len(father) - 1)
    point_2 = randint(1, len(father) - 1)
    child_1 = np.append(father[0: point_1], mother[point_1: point_2])
    child_1 = np.append(child_1, father[point_2: len(father)])
    child_2 = np.append(mother[0: point_1], father[point_1: point_2])
    child_2 = np.append(child_2, mother[point_2: len(mother)])
    childs = cross_revisor(custumers, [child_1.tolist(), child_2.tolist()], qtd_vehicles)
    child_1 = childs[0]
    child_2 = childs[1]
    return child_1, child_2


def simple_random_cross(pop, father, mother, dist_matrix, qtd_vehicles, custumers):
    father = pop[father]
    mother = pop[mother]
    offspring = list(father)
    mother_subroutes = get_routes_per_vehicle(mother, len(mother))
    subroute = mother_subroutes[randint(0, len(mother_subroutes)-1)]
    if len(mother_subroutes) > 1:
        for i in range(len(subroute)):
            offspring.remove(subroute[i])
        offspring_subroutes = get_routes_per_vehicle(offspring, len(offspring))
        sub_off_index = int(randint(0, len(offspring_subroutes)-1))
        off_subroute = offspring_subroutes[sub_off_index]
        offspring_subroutes.pop(sub_off_index)
        route, best_ind = best_insertion(off_subroute, subroute, dist_matrix)
        off_subroute.insert(best_ind, subroute)
        offspring_subroutes.insert(sub_off_index, np.hstack(off_subroute))
        childs = cross_revisor(custumers, [get_individual_from_vehicle(offspring_subroutes, qtd_vehicles)], qtd_vehicles)
        child_1 = childs[0]
        return np.array(child_1)
    else:
        return np.array(mother)


def ordered_cross(father, mother):
    trucks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    father = np.array(father).tolist()
    mother = np.array(mother).tolist()

    def cross(ind1, ind2):
        size = min(len(ind1), len(ind2))
        n1, n2 = 0, 0
        for i in range(size):
            if ind1[i] == '#':
                ind1[i] = trucks[n1]
                n1 += 1
            if ind2[i] == '#':
                ind2[i] = trucks[n2]
                n2 += 1
        a, b = sample(xrange(size), 2)
        if a > b:
            a, b = b, a
        holes1, holes2 = [True] * size, [True] * size
        for i in range(size):
            if i < a or i > b:
                holes1[i] = False
            else:
                holes2[ind2.index(ind1[i])] = False
        child = ['0'] * size
        temp2 = []
        for i in range(size):
            if holes1[i]:
                child[i] = ind1[i]
            if holes2[i]:
                temp2.append(ind2[i])
        j = 0
        for i in range(size):
            if child[i] == '0':
                child[i] = temp2[j]
                j += 1
        for i in range(size):
            if child[i] in trucks:
                child[i] = '#'
        return child
    child_1 = cross(father, mother)
    child_2 = cross(mother, father)
    return child_1, child_2


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
    fitness_father = fitness_ind(father, dist_matrix, qtd_customers, qtd_vehicles, demands, capacity, gama, size_ind)
    fitness_mother = fitness_ind(mother, dist_matrix, qtd_customers, qtd_vehicles, demands, capacity, gama, size_ind)
    if fitness_father > fitness_mother:
        temp = mother
        mother = father
        father = temp

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

    while (routes_father or routes_mother) and (len(child) <= qtd_vehicles - 2):
        # verificaçao no while por que podem ser 
        # adicionados 2 pais a cada iteracao
        # o que pode quebrar o algoritmo, colocando rotas a mais.
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
    
        # child[qtd_vehicles].extend(child[qtd_vehicles + 1 - falta cross 3])
    tmp_child = child[:]
    child = np.array(child)
    try:
        child = np.hstack(child.flat)
    except IndexError:
        print("pai", father)
        print("mae", mother)
        print("child", child)
    lefting_customers = set(father) - set(child)
    lefting_customers = list(lefting_customers)
    lefting_customers.remove('#')
    if lefting_customers:
        if qtd_vehicles == len(tmp_child):
            for item in lefting_customers:
                route, position = best_insertion(tmp_child, item, dist_matrix)
                tmp_child[route].insert(position, item)
        else:
            tmp_child.append(lefting_customers)
    return get_individual_from_vehicle(tmp_child, qtd_vehicles)





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
    # print 'individuo', individual
    individual[pontos[0]] = individual[pontos[1]]
    individual[pontos[1]] = aux
    return individual


# Acao: "Mutacao" do tipo Reversa, tese de 2004 (pag 27)
def reverse_mutation(individual, size_ind, qtd_vehicles):
    # fix-me passar len(individual) como parametro
    rotas = get_routes_per_vehicle(individual, size_ind)
    veiculo = randint(0, len(rotas)-1)
    rota = rotas[veiculo]
    rota_aux = []
    for cliente in xrange(len(rota)):
        rota_aux.append(rota[len(rota)-1-cliente])
    rotas[veiculo] = rota_aux
    return get_individual_from_vehicle(rotas, qtd_vehicles)


# Acao: Mutacao Simples com PayOff de melhor insercao
# tese de 2004 secao 4.3.1 - falta cross 3
def simple_mutation(individual, dist_matrix, qtd_vehicles):
    # sorteia um veiculo e um cliente e o deleta
    #fix-me arrumar o len(individual), passa como parametro
    rotas = get_routes_per_vehicle(individual, len(individual))
    veiculo = randint(0, len(rotas)-1)
    cliente = choice(rotas[veiculo])
    rotas[veiculo].remove(cliente)
    # fix-me os erros nessa mutacao ocorrem por que voce
    # remove um cara, não sei como isso afeta o desempenho,
    # mas eu tirei. da uma olhada aqui
    # sorteia novamente um veiculo (rota) e procura pela menor distancia a
    # partir do cliente escolhido anteriormente
    veiculo = randint(0, len(rotas)-1)
    posicao = best_insertion(rotas[veiculo], [int(cliente)], dist_matrix)
    rota = rotas[veiculo]
    try:
        rota.insert(posicao[1], cliente)
    except IndexError:
        rota.append(cliente)
    rotas[veiculo] = rota
    return get_individual_from_vehicle(rotas, qtd_vehicles)


# Acao: Dado um vetor de clientes (rota) e um cliente de partida
# retorna o cliente de menor distancia ate ele
# Parametros: uma rota e um cliente de partida, devolve o cliente
# mais perto do destino - Teste Best Insertion com PayOff 2004
def best_insertion(routes, client, dist_matrix):
    destino = []
    # cliente = [client]
    cliente = client
    closer = (2*np.amax(dist_matrix)) * - 1
    k1 = int(cliente[0])
    kn = int(cliente[len(cliente)-1])
    for veiculo in range(len(routes)):
        rotas = list(routes[veiculo])
        rotas.insert(0, 1)
        i = 0
        while (i < len(rotas)-1):
            cm = int(rotas[i])
            cm1 = int(rotas[i+1])
            payoff = dist_matrix[cm][cm1] - dist_matrix[cm][k1] - dist_matrix[kn][cm1]
            # maior payoff
            if payoff > closer:
                closer = payoff
                # rota, posição na rota
                destino = veiculo, i
            i = i + 1
    return destino


# =-=-=-=-=-=-=-=-=-=-=- BIGGEST OVERLAP CROSSOVER INI =-=-=-=-=-=-=-=-=-=-=-=- #
# Acao: Calculo do Bounding Box por Rota
# Recebe um individuo e retorna um vetor com os 4 pontos da sua caixa
def bounding_box(individual, customers):
    coordenadas = []
    size = len(individual)
    rotas = get_routes_per_vehicle(individual, size)
    # pontos dos clientes por rota
    for veiculo in xrange(len(rotas)):
        vetor_x = []
        vetor_y = []
        rota = rotas[veiculo]
        rota.insert(0, 1)
        for cliente in rota:
            vetor_x.append(customers[int(cliente)-1][1])
            vetor_y.append(customers[int(cliente)-1][2])
        max_x, max_y = max(vetor_x), max(vetor_y)
        min_x, min_y = min(vetor_x), min(vetor_y)
        # coordenadas.append([(max_x, max_y), (max_x, min_y),
                            # (min_x, min_y), (min_x, max_y)])
        coordenadas.append([(min_x), (max_x), (min_y), (max_y)])
    return coordenadas

def intersect_area(individual, customers):
    area = []
    intersect = bounding_box(individual, customers)
    for rota in range(len(intersect)):
        for rota1 in range(len(intersect) - 1 - rota):
            left = max(intersect[rota][0], intersect[rota+rota1+1][0])
            right = min(intersect[rota][1], intersect[rota+rota1+1][1])
            bottom = max(intersect[rota][2], intersect[rota+rota1+1][2])
            top = min(intersect[rota][3], intersect[rota+rota1+1][3])
            if left < right and bottom < top:
                overlap = (int(right - left) * int(top - bottom))
                area.append((overlap, rota, (rota+rota1+1)))
            else:
                area = distancia_centroides()
    return area

def distancia_centroides(individual, customers):
    centroides = bounding_box(individual, customers)
    dist_centroides = []
    for rota in range(len(centroides)):
        for rota1 in range(len(centroides) - 1 - rota):
            dist = ec((((centroides[rota][1] + centroides[rota][0]) / 2), \
                     ((centroides[rota][3] + centroides[rota][2]) / 2)),
                     (((centroides[rota+rota1+1][1] + centroides[rota+rota1+1][0]) / 2), \
                     ((centroides[rota+rota1+1][3] + centroides[rota+rota1+1][2]) / 2)))
            dist_centroides.append((dist, rota, (rota+rota1+1)))
    return dist_centroides

def biggest_overlap():

    pass

# =-=-=-=-=-=-=-=-=-=-=- BIGGEST OVERLAP CROSSOVER FIM =-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

# Tenho frescuras e preciso arrumar codigos feios FIX-ME
def elitims(tx_elitims, pop, size_pop):
    qtd = int((tx_elitims * size_pop))
    # 0 no lamba por que o fitness, é o primeiro elemento de um item
    # de pop
    # ja chega aqui ordenado
    pop = sorted(pop, key=lambda x: x[1])
    return_pop = pop[:qtd]
    list_pop = []
    for item in return_pop:
        list_pop.append(item[0])
    return list_pop


# Recebe o resultado de um crosssover e checa se eh factivel
# Devolve uma rota corrigida
def cross_revisor(custumers, childs, qtd_vehicles):
    for i in range(len(childs)):
        offspring = childs[i]
        repeated = np.zeros(len(custumers) + 1)
        # Conta clientes repetidos
        for x in offspring:
            if x != '#':
                repeated[int(x)] += 1
        # Apaga o primeiro repetido que encontrar no vetor
        for x in range(len(repeated)):
            if repeated[x] > 1:
                offspring.remove(str(x))
        # verifica se todos os clientes estão na rota,
        # se não, insere aleatoriamente
        for j in custumers[1:len(custumers)]:
            if str(j) not in offspring:
                offspring.insert(randint(0, len(offspring)-1), str(j))
        trucks = [x for x in offspring if x == '#']
        n_trucks = len(trucks)
        while n_trucks < qtd_vehicles - 1:
            offspring.insert(randint(0, len(offspring)-1), '#')
            n_trucks += 1
        n_trucks = len(trucks)
        while n_trucks > qtd_vehicles - 1:
            offspring.remove('#')
            n_trucks -= 1
        childs[i] = offspring
    return childs


def evolve(pop, params, dist_matrix, qtd_customers,
           qtd_vehicles, demands, capacity, gama, size_ind, fit_pop, customers):
    new_pop = []

    max_fitness = max(fit_pop)
    min_fitness = min(fit_pop)
    total_fitness = sum(fit_pop)
    new_pop.extend(elitims(params['taxa_elitismo'], pop, params["tamanho_pop"]))
    # print('ramanhopop', params['tamanho_pop'])
    count = 0
    # fix-me colocar a quantidade de 
    # individuos da populacao auqi
    while count < params['tamanho_pop']:
        index_p1 = roleta(pop, fit_pop, max_fitness,
                          min_fitness, total_fitness)
        index_p2 = roleta(pop, fit_pop, max_fitness,
                          min_fitness, total_fitness)
        father = pop[index_p1]
        mother = pop[index_p2]
        child = simple_random_cross(pop, index_p1, index_p2, dist_matrix, qtd_vehicles, customers)
        if params['taxa_mutacao'] > random():
            child = simple_mutation(child, size_ind, qtd_vehicles)
        new_pop.append(child)
        count += 1
    return new_pop


# Acao: Roleta para minimizacao
# Parametro: Populacao
def roleta(populacao, fitness, max_fitness, min_fitness, fitness_total):
    # gera um valor aleatorio dentro do range fitness total
    aleatorio = random()*fitness_total
    # range entre maior e menor para usar na roleta de minimizacao
    range_fitness = max_fitness + min_fitness
    # Minimizacao = http://stackoverflow.com/questions/8760473/
    size_pop = len(populacao)
    for index in xrange(size_pop):
        # o range - o fitness do individuo eh subtraido do valor
        # aleatorio gerado ate que este seja < 0
        aleatorio -= (range_fitness - fitness[index])
        if aleatorio <= 0:
            return index
    return size_pop - 1


def plot_graph(betters, means, stdr_dev, procriation, path):
    plot_lines = []
    plt.title("Genetic Algorithm ")
    plt.plot(procriation[1:], betters[1:], color='blue', linewidth=4, linestyle='-')
    plt.plot(procriation[1:], means[1:], color='green', linewidth=4, linestyle='-.')
    plt.plot(procriation[1:], stdr_dev[1:], color="red", linewidth=4, linestyle='--')

    blue_line = mlines.Line2D([], [], color='blue')
    green_line = mlines.Line2D([], [], color='green')
    red_line = mlines.Line2D([], [], color='red')
    plot_lines.append([blue_line, green_line, red_line])

    legend1 = plt.legend(plot_lines[0], ["Best Fitness", "Mean Fitness", "Standart Deviation"], loc=1)
    plt.grid(True)
    plt.autoscale()
    plt.gca().add_artist(legend1)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    # plt.show()
    plt.savefig(path + "grafico_evolucao.eps")
    plt.savefig(path + "grafico_evolucao.png")
    plt.close()


def clean_str(string):
    remove = ['\'', ']', '[', '(', ')', ',', ' ']
    for item in remove:
        string = string.replace(item, "")
    return string


def plot_route(ind, coords, path):
    routes = get_routes_per_vehicle(ind, len(ind))
    x_coord = coords[:, 0]
    y_coord = coords[:, 1]
    plt.figure(1)
    plt.title("Melhor Rota")
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y', 'k', 'c', 'm'])))
    for route in routes:
        # todo mundo comeca na posicao 0 do vetor de 
        # coordenadas
        route_coord_x = [int(x_coord[0])]
        route_coord_y = [int(y_coord[0])]
        for item in route:
            # fix-me é isso mesmo aqui no indice?
            route_coord_x.append(x_coord[int(item) - 1])
            route_coord_y.append(y_coord[int(item) - 1])
        # todo mundo volta pra posicao 0
        route_coord_x.append(int(x_coord[0]))
        route_coord_y.append(int(y_coord[0]))
        plt.plot(route_coord_x, route_coord_y, 'o-')

    plt.savefig(path + "Melhor_rota.png")
    plt.savefig(path + "Melhor_rota.eps")
    plt.close()


def tournament(fit_pop, k):
    selecteds = []
    for _ in range(k):
        index = randint(0, len(fit_pop) - 1)
        selecteds.append((fit_pop, index))

    return min(selecteds, key=itemgetter(0))[1]


def main():
    # clientes com suas localidades vem do arquivo de teste
    # Lê arquivo de teste
    customers, qtd_customers, qtd_vehicles, capacity =\
            load('tests/A-n32-k5_1.vrp')
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
    for i in xrange(geracoes):
        fit_pop = fitness_pop(pop, dist_matrix, qtd_customers,
                           qtd_vehicles, demands, capacity, gama, size_ind)

        fit_history.append(min(fit_pop))
        pop = evolve(pop, params, dist_matrix, qtd_customers,
                qtd_vehicles, demands, capacity, gama, size_ind, fit_pop, cstrs_list)
        if i % 100 == 0:
            print("########### geracao", i)
    print("melhor", np.min(fit_history[-1]))

if __name__ == '__main__':
    main()
