import numpy as np
import time

def loadMatrix(fileName):
    #Conversion des données dans un tableau 2**N x 2**N
    data = np.loadtxt(fileName, skiprows = 1)

    return data



def standardProduct(A, B, N):
    size = 2**N
    result = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            coeff = 0
            for k in range(size):
                coeff += A[i][k]*B[k][j]
            result[i][j] = coeff

    return result



def strassenProduct(A, B, N, seuil):
    if(N <= seuil):
        return standardProduct(A, B, N)
    else:
        half_size = 2**(N-1)
        size = 2**N

        A1 = A[0:half_size, 0:half_size]
        A2 = A[0:half_size, half_size:size]
        A3 = A[half_size:size, 0:half_size]
        A4 = A[half_size:size, half_size:size]

        B1 = B[0:half_size, 0:half_size]
        B2 = B[0:half_size, half_size:size]
        B3 = B[half_size:size, 0:half_size]
        B4 = B[half_size:size, half_size:size]

        M1 = strassenProduct(A3 + A4 - A1, B4 - B2 + B1, N-1, seuil)
        M2 = strassenProduct(A1, B1, N-1, seuil)
        M3 = strassenProduct(A2, B3, N-1, seuil)
        M4 = strassenProduct(A1 - A3, B4 - B2, N-1, seuil)
        M5 = strassenProduct(A3 + A4, B2 - B1, N-1, seuil)
        M6 = strassenProduct(A2 - A3 + A1 - A4, B4, N-1, seuil)
        M7 = strassenProduct(A4, B1 + B4 - B2 - B3, N-1, seuil)

        C1 = M2 + M3
        C2 = M1 + M2 + M5 + M6
        C3 = M1 + M2 + M4 - M7
        C4 = M1 + M2 + M4 + M5

        L1 = np.concatenate((C1, C2), axis=1)
        L2 = np.concatenate((C3, C4), axis=1)

        return(np.concatenate((L1, L2), axis=0))



def printMatrix(A, N):
    size = 2**N
    for i in range(size):
        for j in range(size):
            print(int(A[i][j]), " ")
        print("\t")




A = loadMatrix("./mat/A.txt")
B = loadMatrix("./mat/B.txt")


N = 2
seuil = 1

M = standardProduct(A, B, N)
print(M)

P = strassenProduct(A, B, N, seuil)
print(P)