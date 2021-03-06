import math as m
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

# Acao: Calcula distancia euclidiana de um vetor de 2 posicoes com inteiros
# parametros: a eh do tipo [int, int]  assim como b
def euclidian(a, b):
    a = [int(x) for x in a]
    b = [int(x) for x in b]

    return Decimal((m.sqrt(m.pow((a[0] - b[0]), 2) + m.pow(a[1] - b[1], 2))), 2).quantize(0, ROUND_HALF_UP)
