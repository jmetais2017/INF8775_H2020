import numpy as np
import time


def progDyn(C, notes):
    start = time.time()

    n = len(notes)

    J = np.zeros((n, 5), dtype=int)
    fingers = np.zeros((n, 5), dtype=int)

    # Remplissage du tableau
    k = n - 2  # Condition terminale : J[n-1][d] = 0 pour tout d
    while k >= 0:
        for d in range(5):
            # Relation de récurrence
            options = [C[notes[k], d, notes[k + 1], dprime] +
                       J[k + 1][dprime] for dprime in range(5)]
            bestChoice = np.argmin(options)

            # on stocke le meilleur choix à partir de la case courante, pour pouvoir retracer la solution
            fingers[k][d] = bestChoice
            J[k][d] = options[bestChoice]
        k -= 1

    # Reconstruction de la solution
    solution = []

    bestChoice = np.argmin(J[0])
    totalCost = J[0][bestChoice]

    for k in range(n):
        solution.append(bestChoice)
        bestChoice = fingers[k][bestChoice]

    end = time.time()

    return end - start, totalCost, solution
