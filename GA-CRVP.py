# Representação do invididuo deve serguir a forma:
# [[costumer#1, costumer#2, costumer#n, fitness, vehicle],
# [costumer#1, costumer#2, costumer#n, fitness, vehicle],
# [costumer#1, costumer#2, costumer#n, fitness, vehicle]]
#
# onde,
#
# * A quantidade de linhas dessa matriz, sera a quantidade
# de veiculos
# * Os campos veiculos e fitness serao fixos
# * Somente os clientes sofrerao os operadores
# * O fitness de cada cromossomo(Consideraremos cromossomo
# como sendo cada linha da matriz) sera atualizado a cada
# alteracao que o cromossomo sofra
# * O fitness do invididuo sera a soma do fitness de cada
# cromossomo

# Os parametros para a execucao geral do algoritmo
# devem vir de um arquivo parameters.json que deve
# estar na mesma pasta que este script


import numpy as np


# Acao: Gera um cromossomo
# parametros: qtd_vehicles, qtd_costumers
def generate_cromossome(vehicle, qtd_costumers):
    crm = np.random.randint(1, qtd_costumers + 1, size=qtd_costumers)
    crm = np.append(crm, [0])
    crm = np.append([0], crm)
    crm = np.append(crm, [vehicle])
    # crm = np.append(crm, [fitness]) #todo calc fitness
    return crm


# Acao: Gera um indiviuo
# parametros: qtd_vehicles, qtd_costumers
def generate_individual(qtd_vehicles, qtd_costumers):
    individual = []
    for vehicle in range(qtd_vehicles):
        individual.append(generate_cromossome(vehicle, qtd_costumers))
    return np.array(individual)


print(generate_individual(5, 10))
