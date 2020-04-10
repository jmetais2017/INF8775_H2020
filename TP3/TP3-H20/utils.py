# This class his used to implement specific data structure

class Node:

    def __init__(self, id, cured, value=None, cost=None):
        self.id = id
        self.cured = cured
        self.value = value
        self.cost = cost

    def getId(self):
        return self.id

    def getCured(self):
        return self.cured

    def getValue(self):
        return self.value

    def getCost(self):
        return self.cost

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
