import math as m


# Acao: Calcula distancia euclidiana de um vetor de 2 posiçoes com inteiros
# parametros: a é do tipo [int, int]  assim como b
def euclidian(a, b):
    return m.sqrt(m.pow((a[0] - b[0]), 2) + m.pow(a[1] - b[1], 2))

