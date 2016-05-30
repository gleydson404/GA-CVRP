import math as m


def euclidian(a, b):
    return m.sqrt(m.pow((a[0] - b[0]), 2) + m.pow(a[1] - b[1], 2))

print (euclidian((1,2), (2, 3)))
