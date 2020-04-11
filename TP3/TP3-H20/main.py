import os
import sys
from Population import Population
from Algo import Algo

K = 3 # Entre 2 et 5
EXEMPLAIRE = '100_4950_25_0.txt'

# Generer des exemplaire
def generateEchantillon(relation, proportion):
    N = [100, 500, 1000]
    for n in N:
        if relation == 'min':
            r = 10*n

        if relation == 'max':
            r = (n*(n-1)) / 2

        if proportion == 'min':
            p = 5

        if proportion == 'max':
            p = 25

        parameters = '-N ' + str(n) + ' -r ' + str(int(r)) + ' -p ' + str(p)
        os.system('C:/anaconda/python generator.py ' + parameters)


# generateEchantillon('min', 'min')
# generateEchantillon('min', 'max')
# generateEchantillon('max', 'min')
# generateEchantillon('max', 'max')

# First define the population
population = Population(EXEMPLAIRE)

# Get the current situation
population.load_exemplaire()

# Get the current level of contagion
nb_contamine = population.propagateInfection(K)

print("niveau de contamination: %.2f" %int(nb_contamine/population.size))

# Do we need to act
if nb_contamine / population.getSize() < 0.5:
    sys.exit()

# Get the relations
population.buildRelation()

# The BranchAndBound class his responsible to find the optimal solution
algo = Algo(population.getLevelGraph(), population.getContaminedBy())

# Build the tree that defines the propagation path
algo.propagationTree(population.getRelations())

# After we grade the virus propagators
algo.gradePropagators(K)

# Then we cut links
linkToBreak = algo.branchAndBound(population.size, K)

print(nb_contamine)