import numpy as np
import random as rd

from glouton import glouton
from progDyn import progDyn
from localSearch import localSearch
from utils import *

# Chargement du tenseur de transitions
load_file = np.loadtxt('cout_transition.txt', dtype=int)
cout_transition = load_file.reshape((24, 5, 24, 5))

# Chargement de l'exemplaire
notes = np.loadtxt("./Chansons/fur_elise.txt", skiprows=1, dtype=int)

gloutonTime, gloutonCost, gloutonSol = glouton(cout_transition, notes)

progDynTime, progDynCost, progDynSol = progDyn(cout_transition, notes)

localSearchTime, localSearchCost, localSearchSol = localSearch(
    cout_transition, notes)

print(localSearch(cout_transition, notes, gloutonSol, 100))
