import os
import sys
import argparse
from Population import Population
from Algo import Algo

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--E", help="chemin_vers_exemplaire")
parser.add_argument("-k", "--relations", type=int, help="taux_de_propagation")
parser.add_argument("-p", "--print", type=bool, help="Affiche les liens", required=False, default=False)
args = parser.parse_args()

EXEMPLAIRE = args.E[1:-1]
K = args.relations
print_relation = args.print


# K = 3 # Entre 2 et 5
# EXEMPLAIRE = '500_5000_25_0.txt'
# print_relation = False

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

print("Niveau de contamination si rien est fait (en pourcentage): %.2f " % (int(nb_contamine/population.size)*100))

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
linkToBreak = algo.branchAndBound(population.size, K, print_relation)

print(nb_contamine)