import numpy as np
import time
import sys
import math

from algos import loadMatrix
from algos import printMatrix
from algos import runStandardProduct
from algos import runStrassenProduct


algo = sys.argv[1]

A = loadMatrix(sys.argv[2])
B = loadMatrix(sys.argv[3])

printMat = sys.argv[4]
printTime = sys.argv[5]

N = int(math.log(np.size(A, 0), 2))
seuil = 0

if (algo == "conv"):
    M, duration = runStandardProduct(A, B, N)
elif (algo == "strassen"):
    M, duration = runStrassenProduct(A, B, N, seuil)
elif (algo == "strassenSeuil"):
    seuil = 3
    M, duration = runStrassenProduct(A, B, N, seuil)
else:
    print("Please specify algorithm : conv, strassen or strassenSeuil")

if printMat=="1":
    printMatrix(M, N)
if printTime=="1":
    print(1000.0*duration)
