#!/bin/python

import numpy as np
from numpy.linalg import svd
import givens
import itertools
import pickle, sys
from itertools import combinations

ANGS_TABLE = {}
LTABLE = {}

ANGS_TABLE_FILE = ".kll-angs-table-file"
LTABLE_FILE = ".kll-ltable-file"

def generate_data_lookup(NUMBER_OF_ANGLES = 10, MATRIX_SIZE = 5):
    global ANGS_TABLE, LTABLE

    ANGLES = np.arange(0,2*np.pi,2*np.pi/NUMBER_OF_ANGLES)

    ANGS_TABLE = {}

    print "generating angles table"
    
    for ang in ANGLES:
        ANGS_TABLE[ang] = np.identity(MATRIX_SIZE)
        for i,j in combinations(xrange(MATRIX_SIZE),2):
            ANGS_TABLE[ang] = np.dot(ANGS_TABLE[ang],givens.givens(i,j,ang,MATRIX_SIZE))
        #print ang,ANGS_TABLE[ang]

    LTABLE = {}

    print "generating ltable"
    number_of_entries = NUMBER_OF_ANGLES**(MATRIX_SIZE-1)
    print "number of entries: %u"%(number_of_entries)
    i = 0
    for angs in itertools.product(ANGS_TABLE,repeat=MATRIX_SIZE-1):
        i+=1
        if (i%(number_of_entries/100) == 0):
            sys.stdout.write('.')
	    sys.stdout.flush()
        MAT = np.identity(MATRIX_SIZE)
        for ang in angs:
            MAT = np.dot(MAT,ANGS_TABLE[ang])
        LTABLE[angs] = MAT
    
    pickle.dump(ANGS_TABLE,open(ANGS_TABLE_FILE,"wb"), protocol = 2)
    pickle.dump(ANGS_TABLE,open(LTABLE_FILE,"wb"), protocol = 2)
    
    print len(ANGS_TABLE), len(LTABLE)
    
def read_data_lookup_file():
    global ANGS_TABLE, LTABLE

generate_data_lookup()

int_vec = np.vectorize(int)

def find_angles(M):
    less = ((0,0,0,0),25)
    for angles in LTABLE:
        mat = LTABLE[angles]
        D = np.dot(mat,M.transpose())
        abs_vec = np.vectorize(abs)
        s = abs_vec(D).sum()
        if s <= less[1]:
            less = (angles,s)
        #if less[1] < 25:
            #return less[0]
    return less[0] 

def mat_recuperate(au,av,s):
    U = LTABLE[au]#.transpose()
    V = LTABLE[av]#.transpose()
    S = np.diag(s)
    return np.dot(U,np.dot(S,V))

def compact_data(data):
    x = np.array(data)
    A = np.matrix(np.array_split(x,5))
    print A

    U, s, V = svd(A)

    print U
    print V
    
    au = find_angles(U)
    av = find_angles(V)

    print LTABLE[au].transpose()
    print LTABLE[av].transpose()
    
    #print au,av,s

    Ar = mat_recuperate(au,av,int_vec(s))

    Ar2 = np.dot(U,np.dot(np.diag(int_vec(s)),V))
    print int_vec(Ar)
    print int_vec(Ar2)

    #print A - Ar

import random

data = [random.randint(0,2**8) for _ in range(25)]

compact_data(data)    
