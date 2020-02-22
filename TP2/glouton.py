import numpy as np
import time

def glouton(C, notes):
    start = time.time()

    exSize = len(notes)

    totalCost = 0
    solution = []


    #Initialisation : choix de d0 et d1
    transitions = [C[notes[0], :, notes[1], :]]
    bestCost = np.argmin(transitions) #Récupréation de la transition permettant de passer de la première à la deuxième note ayant le coût le plus faible
    bestd0 = int(bestCost / 5)
    bestd1 = bestCost - 5*bestd0
    bestTransition = transitions[0][bestd0][bestd1]

    solution.append(bestd0)
    solution.append(bestd1)
    totalCost += bestTransition


    #Remplissage de la solution
    for currentId in range(2, exSize):
        bestFinger = np.argmin(C[notes[currentId - 1]][solution[currentId - 1]][notes[currentId]])
        bestTransition = C[notes[currentId - 1]][solution[currentId - 1]][notes[currentId]][bestFinger]

        solution.append(bestFinger)
        totalCost += bestTransition


    end = time.time()

    return end-start, totalCost, solution

