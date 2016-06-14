from GACRVP import *
import numpy as np
import datetime
import time
import csv
import random

customers, qtd_customers, qtd_vehicles, capacity = load('tests/A-n32-k5.vrp')
demands = customers[:, 3]
cstrs_list = customers[:, 0]
params = load_parameters("config.json")
dist_matrix = gen_dist_matrix(qtd_customers, customers)
gama = 1

# pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)

def pokemon(pop, dist_matrix, qtd_customers, qtd_vehicles, capacity, gama, size):
    nova_populacao = [] # recebe elitismo
    filhos = []         # recebe filhos dos crossovers que serao mutados
    # minimo_fitness = [] # apenas para retorno, nao sera mais usado
    pop_plus_fit = []   # Usado na troca da populacao por algum motivo que eu esqueci
    pop_fitness = []    # Vetor de tuplas (individuo, fitness)

    # shufle da populacao, que provavelmente chega aqui ordenada pelo menor fitness
    random.shuffle(pop)

    # calculo o fitness
    fitness_populacao = fitness_pop(pop, dist_matrix, qtd_customers, qtd_vehicles,
                                    demands, capacity, gama, size)

    # Junta individuo (pop) e seu fitness (fitness populacao) em um so vetor
    for i, fitness in enumerate(fitness_populacao):
        pop_fitness.append([pop[i], fitness])

    # ordena de acordo com o fitness
    #pop_fitness = sorted(pop_fitness, key=lambda x: x[1])

    # Aplicacao do elitismo passando vetor de individuo e fitness ja ordenado
    if params['taxa_elitismo'] > 0:
        nova_populacao.extend(elitims(params['taxa_elitismo'], pop_fitness, params['tamanho_pop']))

    # Separa Individuo do fitness
    pop = [individuo[0] for individuo in pop_fitness]
    fitness = [individuo[1] for individuo in pop_fitness]

    # Calculo do Max, Min e total do fitness para usar na roleta
    max_fitness = max(fitness)
    min_fitness = min(fitness)
    total_fitness = sum(fitness)
    print "Melhor Fitness: ", min_fitness
    print "Pior Fitness: ", max_fitness

    # Minimo_fitness servia apenas para retorno, o que acredito que nao sera mais necessario
    # minimo_fitness.append((min_fitness, pop[fitness_populacao.index(min_fitness)]))

    # gera quantos filhos forem necessarios ate que a populacao seja 100 (somado ao elitismo)
    while len(filhos) < (params['tamanho_pop'] - (params['taxa_elitismo'] * params['tamanho_pop'])):
        prob_crossover = np.random.uniform(0, 1)
        if prob_crossover <= params['taxa_crossover']:
            if params['tipo_crossover'] == 1:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 1
                    filhos.extend(simple_one_point_cross
                                  (roleta(pop, fitness, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness, max_fitness, min_fitness, total_fitness),
                                   pop, cstrs_list))

            if params['tipo_crossover'] == 2:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 2
                    filhos.extend(simple_two_points_cross
                                  (pop, roleta(pop, fitness, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness, max_fitness, min_fitness, total_fitness),cstrs_list))

            if params['tipo_crossover'] == 3:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 3
                    filhos.append(simple_random_cross
                                  (pop, roleta(pop, fitness, max_fitness, min_fitness, total_fitness),
                                   roleta(pop, fitness, max_fitness, min_fitness, total_fitness),
                                   dist_matrix, qtd_vehicles, cstrs_list))

            if params['tipo_crossover'] == 4:
                if params['tipo_selecao'] == 1:  # adiciona no final do vetor os filhos retornados pelo crossover 4
                    filhos.append(uniform_cross
                                  (pop[(roleta(pop, fitness, max_fitness, min_fitness, total_fitness))],
                                   pop[(roleta(pop, fitness, max_fitness, min_fitness, total_fitness))],
                                   dist_matrix, qtd_customers, qtd_vehicles, gama, demands, capacity, size))

        else:
            if params['tipo_selecao'] == 1:
                filhos.append(pop[roleta(pop, fitness, max_fitness, min_fitness, total_fitness)])
                filhos.append(pop[roleta(pop, fitness, max_fitness, min_fitness, total_fitness)])

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
    # Mantem apenas nova geracao
    if params['troca_populacao'] == 1:
        nova_populacao = nova_populacao + filhos
    # Junta as duas populacoes, ordena pelo fitness e exclui os piores individuos (nazi) - diminui a diversidade
    else:
        nova_populacao = nova_populacao + filhos + pop

    #fitness da nova populacao
    novo_fitness = fitness_pop(nova_populacao, dist_matrix, qtd_customers, qtd_vehicles,
                               demands, capacity, gama, size)
    #concatena em vetor de tuplas
    for i, fitness in enumerate(novo_fitness):
        pop_plus_fit.append([nova_populacao[i], fitness])
    # ordena de acordo com o fitness
    pop_plus_fit = sorted(pop_plus_fit, key=lambda x: x[1])
    # Separa Individuo do fitness
    nova_populacao = [individuo[0] for individuo in pop_plus_fit[:params['tamanho_pop']]]
    novo_fitness = [individuo[1] for individuo in pop_plus_fit[:params['tamanho_pop']]]

    #Neste momento, todos os vetores usados sao listas
    return nova_populacao, novo_fitness

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-
execucao = 0
fitness_execucoes = []

while execucao < params['execucao']:
    pop = gen_pop(params['tamanho_pop'], qtd_vehicles, qtd_customers, cstrs_list)
    date = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y-%H%M%S')
    procriation = []
    betters = []
    means = []
    worses = []
    resultado = open("" + date + ".csv", "w")
    csvwriter = csv.DictWriter(resultado, params.keys())
    csvwriter.writeheader()
    csvwriter.writerow(params)
    print "execucao: ", execucao
    # resultado.write(str(execucao))
    # resultado.write("\n\n")
    melhor_fit = []
    print "parametros: ", params
    # resultado.write("\n\n")
    # resultado.write(str(params))

    geracao = 0
    while geracao < params['geracoes']:
        size = len(pop[0])
        if geracao % 100 == 0:
            print "geracao: ", geracao
        procriation.append(geracao)
        # resultado.write(str(geracao))
        # resultado.write("\n\n")
        pop, melhor = pokemon(pop, dist_matrix, qtd_customers, qtd_vehicles, capacity, gama, size)
        melhor_fit.extend(melhor)
        geracao = geracao + 1
        # resultado.write(str(melhor))
        # resultado.write("\n")
        betters.append(melhor)
        # means.append(np.mean(pop[:, 0]))
    # melhor = sorted(melhor_fit, key=lambda x: x[0])
    # print "Fitness minimo ever: ", min(melhor_fit, key=lambda t: t[0])
    # min_melhor_fit = min(melhor_fit, key=itemgetter(0))
    # print "Fitness minimo ever: ", min_melhor_fit
    # resultado.write(str(min_melhor_fit))
    # fitness_execucoes.append(min_melhor_fit)
    execucao = execucao + 1
    resultado.close()
# print "Melhor fitness de ", params['execucao'], ": ", min(fitness_execucoes)
