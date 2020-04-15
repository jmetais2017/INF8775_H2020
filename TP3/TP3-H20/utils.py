import os

# This class his used to implement specific data structure
#C:/anaconda/python check_sol.py ./exemplaires/500_5000_25_0.txt results.txt 3
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


# Inspired by https://pythonschool.net/data-structures-algorithms/code/binary_tree.py
# class BinaryTree():
#
#     def __init__(self, id, value=None, left=None, right=None):
#         self.left = left
#         self.right = right
#         self.id = id
#         self.value = value
#
#     def getLeftChild(self):
#         return self.left
#
#     def getRightChild(self):
#         return self.right
#
#     def setNodeValue(self, value):
#         self.id = value
#
#     def getNodeValue(self):
#         return self.id
#
#     def insertRight(self, newNode):
#         if self.right == None:
#             self.right = BinaryTree(newNode)
#         else:
#             tree = BinaryTree(newNode)
#             tree.right = self.right
#             self.right = tree
#
#     def insertLeft(self, newNode):
#         if self.left == None:
#             self.left = BinaryTree(newNode)
#         else:
#             tree = BinaryTree(newNode)
#             self.left = tree
#             tree.left = self.left
#
#     def printTree(self):
#         if self != None:
#             self.printTree(self.getLeftChild())
#             print(self.getNodeValue())
#             self.printTree(self.getRightChild())
#
#     # test tree
#
#     def testTree(self):
#         myTree = BinaryTree("Maud")
#         myTree.insertLeft("Bob")
#         myTree.insertRight("Tony")
#         myTree.insertRight("Steven")
#         self.printTree(myTree)
