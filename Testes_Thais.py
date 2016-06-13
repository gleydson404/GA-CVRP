from GACRVP import *
import pprint
import numpy as np
from Distances import euclidian
from operator import itemgetter
import datetime
import time

customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n32-k5.vrp')
demands = customers[:, 3]
cstrs_list = customers[:, 0]
params = load_parameters("config.json")
dist_matrix = gen_dist_matrix(qtd_customers, customers)
gama = 1

pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)

# print params
# pp = pprint.PrettyPrinter(indent=4)
# for individuo in range(len(pop)):
#     print 'individuo: ', individuo, ': \n'
#     print pp.pprint(pop[individuo])

def pokemon(pop, dist_matrix, qtd_customers, qtd_vehicles, capacity, gama, size):
    nova_populacao = []
    minimo_fitness = []
    filhos = []
    pop_fitness = []
    fitness_populacao = fitness_pop(pop, dist_matrix, qtd_customers, qtd_vehicles,
                                    demands, capacity, gama, size)

    for i, fitness in enumerate(fitness_populacao):
        pop_fitness.append([pop[i], fitness])
    nova_populacao.extend(elitims(params['taxa_elitismo'], pop_fitness, params['tamanho_pop']))

    max_fitness = max(fitness_populacao)
    print "max fitness: ", max_fitness
    min_fitness = min(fitness_populacao)
    minimo_fitness.append((min_fitness, pop[fitness_populacao.index(min_fitness)]))
    # so vai funcionar se houver elitismo
    print "min fitness: ", pop_fitness[0][1]
    total_fitness = sum(fitness_populacao)

    while len(filhos) < (params['tamanho_pop'] - (params['taxa_elitismo'] * params['tamanho_pop'])):
        prob_crossover = np.random.uniform(0, 1)
        if prob_crossover <= params['taxa_crossover']:
            if params['tipo_crossover'] == 1:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 1
                    filhos.extend(simple_one_point_cross
                                  (roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),
                                   pop, cstrs_list))

            if params['tipo_crossover'] == 2:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 2
                    filhos.extend(simple_two_points_cross
                                  (pop, roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),cstrs_list))

            if params['tipo_crossover'] == 3:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 3
                    filhos.append(simple_random_cross
                                  (pop, roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness),
                                   dist_matrix, qtd_vehicles, cstrs_list))

            if params['tipo_crossover'] == 4:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 4
                    filhos.append(uniform_cross
                                  (pop[(roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness))],
                                   pop[(roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness))],
                                   dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity, size))

        else:
            if params['tipo_selecao'] == 1:
                filhos.append(pop[roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness)])
                filhos.append(pop[roleta(pop, fitness_populacao, max_fitness, min_fitness, total_fitness)])

    # Mutacao
    for i, individuo in enumerate(filhos):
        prob_mutacao = np.random.uniform(0, 1)
        if prob_mutacao <= params['taxa_mutacao']:
            if params['tipo_mutacao'] == 1:
                filhos[i] = swap_mutation(individuo)
            if params['tipo_mutacao'] == 2:
                filhos[i] = reverse_mutation(individuo, size, qtd_vehicles)
            if params['tipo_mutacao'] == 3:
                filhos[i] = simple_mutation(individuo, dist_matrix, qtd_vehicles)

    # Troca da Populacao
    if params['troca_populacao'] == 1:
        nova_populacao = nova_populacao + filhos
        # Junta as duas populacoes, ordena pelo fitness e exclui os piores individuos (nazi) - diminui a diversidade
    else:
        nova_populacao = nova_populacao + filhos + pop
        novo_fitness = sorted(fitness_pop(pop, dist_matrix, qtd_customers, qtd_vehicles,
                demands, capacity, gama, size), key=itemgetter(0), reverse=False)
        nova_populacao = [individuo[1] for individuo in novo_fitness[0:(params['tamanho_pop'])]]
    #
    # for i in range(len(pop)):
    #     print nova_populacao[i], fitness_populacao[i]

    return nova_populacao, minimo_fitness

execucao = 0
fitness_execucoes = []

while execucao < params['execucao']:
    pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y-%H%M%S')
    resultado = open("C:\Users\Thais\Documents\GitHub\GA-CVRP\GA-CVRP\Testes\GA_" + date + ".txt", "w")
    print "execucao: ", execucao
    resultado.write(str(execucao))
    resultado.write("\n\n")
    melhor_fit = []
    print "parametros: ", params
    resultado.write("\n\n")
    resultado.write(str(params))

    geracao = 0
    while geracao < params['geracoes']:
        size = len(pop[0])
        print "geracao: ", geracao
        resultado.write(str(geracao))
        resultado.write("\n\n")
        pop, melhor = pokemon(pop, dist_matrix, qtd_customers, qtd_vehicles, capacity, gama, size)
        melhor_fit.extend(melhor)
        geracao = geracao + 1
        resultado.write(str(melhor))
        resultado.write("\n")
    # melhor = sorted(melhor_fit, key=lambda x: x[0])
    # print "Fitness minimo ever: ", min(melhor_fit, key=lambda t: t[0])
    print "Fitness minimo ever: ", min(melhor_fit, key=itemgetter(0))
    resultado.write(str(min(melhor_fit)))
    fitness_execucoes.append(min(melhor_fit))
    execucao = execucao + 1
    resultado.close()
print "Melhor fitness de ", params['execucao'], ": ", min(fitness_execucoes)