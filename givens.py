# -.- encoding:utf-8 -.-

"""
Implementação da Matriz de Rotação de Givens
"""


import numpy as np
from numpy import sin, cos, pi


def givens_value(i,j,c,s,(x,y)):
    """
    Retorna o valor da celula (x,y) da matriz de givens
    """
    if x == y and x != j and x != i:
        return 1
    elif x == y and x == i:
        return c
    elif x == y and x == j:
        return c
    elif x == j and y == i:
        return s
    elif x == i and y == j:
        return -s
    else: 
        return 0

def givens(i,j,teta,size):
    """
    Retorna a matriz de givens em fomarto de uma matriz NUMPY
    """
    c, s = cos(teta), sin(teta)
    return np.matrix([[givens_value(i,j,c,s,(x,y)) for x in xrange(size)] for y in xrange(size)])
