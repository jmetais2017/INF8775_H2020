# coding=utf8
import math
from utils import Node

class Algo:
    # Contructeur pour le graph
    def __init__(self , level_graph, ContaminedBy):
        self.level_graph = level_graph
        self.contaminedBy = ContaminedBy
        self.propagatesTo = None
        self.ratio = {}
        self.cost = {}
        self.potential_gain = {}


    # Builds a tree from the infected poeple to those they affect and follows the propagation path
    def propagationTree(self, relations):
        self.propagatesTo = {'root': self.level_graph[0]}

        for level in range(0, len(self.level_graph)-1):
            # Les noeuds du niveau actuel
            for i in self.level_graph[level]:
                has_contamined = []
                # Est-ce que le noeud actuel a contribuer a la propagation
                for relation in relations[i]:
                    if self.level_graph[level+1].count(relation) > 0:
                        has_contamined.append(relation)
                if len(has_contamined) > 0:
                    self.propagatesTo.update({i: has_contamined})

    '''
    This function grades the propagators links
    
    Gain his determine by how remove a node cures how many persons
    Basically, the more a person spread the virus the more benifits we have to cure him
    Althought, we have to take into account the number off interdictions we need to impose
    '''
    def gradePropagators(self, K):
        total_impacts = {}

        for level in range(1, len(self.level_graph)):
            # For each level of propagation we get the total impact
            for person in self.level_graph[level]:
                # Compute cost to break link
                cost = (len(self.contaminedBy[person])-K)+1
                # self.cost.update({person: cost})

                # determine for each nodes in layer were virus spread how they them self impact others
                # gain = 1 # himself
                # if person in self.propagatesTo:
                #     gain += len(self.propagatesTo[person])
                    # self.potential_gain.update({person: gain})

                # TODO: Calculate gain like branch and bound to all descendents
                total_impacts = [person]
                if person in self.propagatesTo:
                    impacts = self.propagatesTo[person]

                    # for each of them we check if removing connection removes it if it does we check continue going down
                    for impact in impacts:
                        # -1 for node we are removing
                        contaminedBy = len(self.contaminedBy[impact]) - 1

                        # if contamined by lower then K
                        if contaminedBy < K:
                            if impact in self.propagatesTo:
                                impacts.extend(self.propagatesTo[impact])
                            total_impacts.append(impact)

                gain = len(total_impacts)

                # Compute Gain
                ratio = gain/cost
                if ratio in self.ratio:
                    self.ratio[ratio].append(person)
                    continue

                self.ratio.update({ratio: [person]})

    '''
    This is used to order the search in terms of greedy algorithm
    '''
    def defineNodeOrder(self):
        node_order = []
        for key in sorted(self.ratio.keys(), reverse=True):
            node_order.extend(self.ratio[key])
        return node_order

    '''
    The principal behind this algo his to limit the source

    It takes the parameter K which his the ratio for some1 to contract the virus
    It returns the link that are to be remove to keep the infection under 50%
    
    ref : https://en.wikipedia.org/wiki/Branch_and_bound#Pseudocode
    '''
    def branchAndBound(self, size, K):
        # To add queue.insert(0,data) , Timecomplexity O(n)
        # To remove if len(queue)>0: return queue.pop() O(1)
        queue = [Node('', [], len(self.contaminedBy), 0)]
        solution = []
        bound = size*K  # Initial bound
        keys = self.defineNodeOrder()
        # keys = list(self.contaminedBy.keys())
        size_keys = len(keys)
        # Utilisation de ceil pour nombre impair size car condition < (-1)
        # Exemple floor(448,5) < 897/2 < ceil(448,5) -> 448-1 < 448,5 < 449-1 -> 447*2=894 < 897 < 448*2=896
        condition_success = math.ceil(size/2)
        length_first_level = len(self.level_graph[1])

        while len(queue) > 0:
            node = queue.pop()
            k = len(node.id)
            key = keys[k]
            # If Node produces a solution store it and continue

            # Need to compute gain from removing node
            # Using PropagateTo we get direct impacts
            total_impacts = [key]
            if key in self.propagatesTo:
                impacts = self.propagatesTo[key]

                # for each of them we check if removing connection removes it if it does we check continue going down
                for impact in impacts:
                    # -1 for node we are removing
                    # TODO: Change -1 to see if in total_impacts other nodes involved are removed
                    contaminedBy_removed = 1
                    for propagator in self.contaminedBy[impact]:
                        if propagator in node.getCured():
                            contaminedBy_removed += 1

                    contaminedBy = len(self.contaminedBy[impact]) - contaminedBy_removed

                    # if contamined by lower then K
                    if contaminedBy < K:
                        if impact in self.propagatesTo:
                            impacts.extend(self.propagatesTo[impact])
                        total_impacts.append(impact)

            score = len(total_impacts)
            cost = (len(self.contaminedBy[key])-K) + 1  # Cost to cure the person
            temp_list = node.getCured()
            total_impacts.extend(temp_list)
            if node.value - score < condition_success and node.cost + cost < bound:
                solution.append(Node(node.id + '1', total_impacts, node.value - score, node.cost + cost))
                bound = node.cost + cost
                print(bound)
                continue

            # Else branch on Node to produce other Nodes 0 do nothing, 1 remove node
            Next_Node0 = Node(node.id + '0', node.cured, node.value, node.cost)
            Next_Node1 = Node(node.id + '1', total_impacts, node.value - score, node.cost + cost)

            # Check if produced Nodes bound can obtain optimal, if they can obtain optimal add them to queue
            # Two conditions to check:
            # Node already removed? This needs to be check after first level of contamination, and bound cost
            for new_node in [Next_Node0, Next_Node1]:
                # if len(node.id) > len(self.level_graph[1]) and node.cured.count(keys[k+1]) == 1 or \
                #    len(solution) > 0 and solution[-1].cost:
                if k == size_keys - 1 or k < size_keys - 1 and node.cured.count(keys[k+1]) == 1:
                    continue

            # if bound cost , note : python finishes execution if first condition fails
                if new_node.cost < bound:
                    if len(solution) == 1:
                        queue.insert(0, new_node) # Queue
                        continue
                    queue.append(new_node)  # Stack

        print('test')
