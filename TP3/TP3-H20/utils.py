import os

# This class his used to implement specific data structure
class Node:

    def __init__(self, id, cured=[], links=[]):
        self.id = id
        self.cured = cured
        self.links = links
        # self.cost = cost
        # self.value = value

    def getId(self):
        return self.id

    def getCured(self):
        return self.cured

    def getLinks(self):
        return self.links

    # def getCost(self):
    #     return self.cost
    #
    # def getValue(self):
    #     return self.value


# Generer des exemplaire
def generateEchantillon(n, relation, proportion):
    # N = [10]
    # for n in N:
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

# generateEchantillon(10, 'max', 'max')
# generateEchantillon('min', 'min')
# generateEchantillon('min', 'max')
# generateEchantillon('max', 'min')
# generateEchantillon('max', 'max')
