import numpy as np
import random as rd
import time

from utils import *


def localSearch(C, notes, baseSolution, maxIter):
    solution = np.copy(baseSolution)
    start = time.time()

    n = len(solution)

    nbIter = 0
    while nbIter < maxIter:
        # Génération d'un changement aléatoire
        note = rd.randint(0, n - 1)
        finger = rd.randint(0, 4)

        # Calcul des transitions formées
        new = 0
        if(note > 0):
            new += C[notes[note - 1], solution[note - 1], notes[note], finger]
        if(note < n - 1):
            new += C[notes[note], finger, notes[note + 1], solution[note + 1]]
        # Calcul des transitions supprimées
        old = 0
        if(note > 0):
            old += C[notes[note - 1], solution[note - 1],
                     notes[note], solution[note]]
        if(note < n - 1):
            old += C[notes[note], solution[note],
                     notes[note + 1], solution[note + 1]]

        # Si le changement est améliorant, on l'applique
        if new < old:
            solution[note] = finger
            print(old - new, nbIter)

        nbIter += 1

    totalCost = computeTotalCost(solution, C, notes)
    end = time.time()

    return end - start, totalCost, solution
