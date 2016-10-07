import numpy as np
import givens
from itertools import combinations

NUMBER_OF_ANGLES = 10

MATRIX_SIZE = 5

ANGLES = range(0,2*np.pi,2*np.pi/NUMBER_OF_ANGLES)

ANGS_TABLE = {}

for ang in ANGLES:
    ANGS_TABLE[ang] = np.identity(MATRIX_SIZE)
    for i,j in combinations(xrange(SIZE),2):
        ANGS_TABLE[ang] = np.dot(ANGS_TABLE[ang],givens.givens(i,j,ang,MATRIX_SIZE))
        
LTABLE = {}
        
for a,b,c,d in itertools.product(ANGS_TABLE,repeat = MATRIX_SIZE-1):
   
    LTABLE[(a,b,c,d)] = np.dot(a,np.dot(b,np.dot(c,d)))