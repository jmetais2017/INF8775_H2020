# coding=utf8
import numpy as np

class Algo:
    # Contructeur pour le graph
    def __init__(self , level_graph):
        self.level_graph = level_graph
        self.graph = None


    # Builds a tree from the infected poeple to those they affect and follows the propagation path
    def propagationTree(self, relations, size, K):
        self.graph = {'root': self.level_graph[0]}

        for level in range(0, len(self.level_graph)-1):
            # Les noeuds du niveau actuel
            for i in self.level_graph[level]:
                has_contamined = []
                # Est-ce que le noeud actuel a contribuer a la propagation
                for relation in relations[i]:
                    if self.level_graph[level+1].count(relation) > 0:
                        has_contamined.append(relation)
                if len(has_contamined) > 0:
                    self.graph.update({i: has_contamined})


    # This function grades the propagators links
    def gradePropagators(self, relations, size, K):
        return

    '''
    The principal behind this algo his to limit the source

    It takes the parameter K which his the ratio for some1 to contract the virus
    It returns the link that are to be remove to keep the infection under 50%
    '''
    def branchAndBound(self, K):
        return
