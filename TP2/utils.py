import numpy as np

def computeTotalCost(solution, C, notes):
    totalCost = 0

    for i in range(len(solution) - 1):
        totalCost += C[notes[i], solution[i], notes[i+1], solution[i+1]]

    return totalCost