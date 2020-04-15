# coding=utf8
import math
import sys
from utils import Node

class Algo:
    # Contructeur pour le graph
    def __init__(self , level_graph, ContaminedBy):
        self.level_graph = level_graph
        self.contaminedBy = ContaminedBy
        self.propagatesTo = {}
        self.ratio = {}
        self.cost = {}
        self.potential_gain = {}


    # Builds a tree from the infected poeple to those they affect and follows the propagation path
    # Correction needs to include propagation from lower levels
    def propagationTree(self, relations):
        for level in range(1, len(self.level_graph)):
            # Les noeuds du niveau actuel
            for i in self.level_graph[level]:
                has_contamined = []
                # Est-ce que le noeud actuel a contribuer a la propagation
                for relation in relations[i]:
                    if relation in self.contaminedBy[i]:
                        continue
                    for levels in range(1, len(self.level_graph)):
                        if self.level_graph[levels].count(relation) > 0:
                            has_contamined.append(relation)

                if len(has_contamined) > 0:
                    self.propagatesTo.update({i: has_contamined})

    '''
    This function grades the propagators links
    
    Gain his determine by how remove a node cures how many persons
    Basically, the more a person spread the virus the more benifits we have to cure him
    Althought, we have to take into account the number off interdictions we need to impose
    '''
    def gradePropagators(self, relations, K):
        for level in range(1, len(self.level_graph)):
            # For each level of propagation we get the total impact
            for person in self.level_graph[level]:
                total_impacts = [person]
                # if person in self.propagatesTo:
                #     impacts = self.propagatesTo[person]
                #
                #     # for each of them we check if removing connection removes it if it does we check continue going down
                #     for impact in impacts:
                #         # -1 for node we are removing
                #         contaminedBy = len(self.contaminedBy[impact]) - 1
                #
                #         # if contamined by lower then K
                #         if contaminedBy < K:
                #             if impact in self.propagatesTo:
                #                 impacts.extend(self.propagatesTo[impact])
                #             total_impacts.append(impact)
                #
                gain = len(total_impacts)

                # Compute cost to break link and stay cured
                cost = (len(self.contaminedBy[person])-K)+1

                # self.cost.update({person: cost})

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
    def branchAndBound2(self, size, K, print_relation):
        # To add queue.insert(0,data) , Timecomplexity O(n), to remove if len(queue)>0: return queue.pop() O(1)
        queue = [Node('', [], [])]
        solution = []
        bound = sys.maxsize  # Initial bound
        keys = self.defineNodeOrder()
        size_keys = len(self.defineNodeOrder())
        # Utilisation de ceil pour nombre impair size car condition < (-1)
        # Exemple floor(448,5) < 897/2 < ceil(448,5) -> 448-1 < 448,5 < 449-1 -> 447*2=894 < 897 < 448*2=896
        condition_success = math.ceil(size/2)

        exec_counter = 0
        while len(queue) > 0:
            exec_counter += 1
            node = queue.pop()

            k = len(node.id)
            key = keys[k]

            # His the person already cured
            if key in node.getCured():
                queue.append(Node(node.id + '0', node.getCured(), node.getLinks()))
                continue

            # We determine how to cure the current person
            total_cured = [key]
            if key in self.propagatesTo and key in self.contaminedBy:
                peopleIShouldAvoid = self.propagatesTo[key] + self.contaminedBy[key]
            else:
                peopleIShouldAvoid = self.contaminedBy[key]

            # Remove already cured from the peopleToAvoid since they are not contagious
            temp_list =[]
            for person in peopleIShouldAvoid:
                if person in node.getCured():
                    temp_list.append(person)
            for person in temp_list:
                peopleIShouldAvoid.remove(person)

            # Check if removing link also removes another person
            links_to_break = []
            person_also_cured = []
            for person in peopleIShouldAvoid:
                # Check if it his some1 already contagious then only option his to remove link
                if person in self.level_graph[0]:
                    links_to_break.append((key, person))
                    continue

                # Check if current node removes person, basically if key doesnt get virus this person won't also
                if person in self.propagatesTo and person in self.contaminedBy:
                    person_contagion = self.propagatesTo[person] + self.contaminedBy[person]
                else:
                    person_contagion = self.contaminedBy[person]

                # Find already cured
                person_contagion_cured = []
                for p in person_contagion:
                    if p in node.getCured() or p == key:
                        person_contagion_cured.append(p)
                # get current lvl of infection
                for p in person_contagion_cured:
                    person_contagion.remove(p)

                if len(person_contagion) < K:
                    person_also_cured.append(person)
                else:
                    links_to_break.append((key, person))

            # Else Break link (make sure to break link in this order person_also_cured, propagatesTo, contaminedBy)
            for p in person_also_cured:
                total_cured.append(p)
                peopleIShouldAvoid.remove(p)

            # Right now we are removing all connections
            for index in range(len(peopleIShouldAvoid) + 1 - K, len(links_to_break)):
                links_to_break.pop()

            total_cured.extend(node.getCured())
            links_to_break.extend(node.getLinks())

            # If Node produces a solution store it and continue
            if size - len(total_cured) < condition_success:
                # His the new solution better
                if len(links_to_break) < bound:
                    solution.append(Node(node.id + '1', total_cured, links_to_break))
                    bound = len(links_to_break)
                    if print_relation:
                        not_empty = True if len(solution) > 1 else False
                        self.print_relation(solution[-1], not_empty)
                        continue
                    print(str(bound) + '\n')
                    continue
                # If it's not better stop there and dont consider
                continue

            # Else branch on Node to produce other Nodes 0 do nothing, 1 remove node
            Next_Node0 = Node(node.id + '0', node.getCured(), node.getLinks())
            Next_Node1 = Node(node.id + '1', total_cured, links_to_break)

            # Check if produced Nodes bound can obtain optimal, if they can obtain optimal add them to queue
            # Two conditions to check:
            # First check if we try all node for this combination
            for new_node in [Next_Node0, Next_Node1]:
                if k == size_keys - 1:
                    continue

            # Second if bound cost lower then bound continue
                if len(new_node.getLinks()) < bound:
                    # if len(solution) == 1:
                    #     queue.insert(0, new_node)  # Queue
                    #     continue
                    queue.append(new_node)  # Stack



    def branchAndBound(self, size, K, print_relation):
        # To add queue.insert(0,data) , Timecomplexity O(n), to remove if len(queue)>0: return queue.pop() O(1)
        queue = [Node('', [], size, 0)]
        solution = []
        bound = sys.maxsize  # Initial bound
        keys = self.defineNodeOrder()
        size_keys = len(keys)
        # Utilisation de ceil pour nombre impair size car condition < (-1)
        # Exemple floor(448,5) < 897/2 < ceil(448,5) -> 448-1 < 448,5 < 449-1 -> 447*2=894 < 897 < 448*2=896
        condition_success = math.ceil(size/2)

        exec_counter = 0
        while len(queue) > 0:
            exec_counter += 1
            node = queue.pop()
            k = len(node.id)
            key = keys[k]

            # His the node already gone
            if key in node.getCured():
                queue.append(Node(node.id + '0', node.cured, node.value, node.cost))
                continue

            # Need to compute gain from removing node
            # Using PropagateTo we get direct impacts
            total_impacts = [key]
            if key in self.propagatesTo:
                impacts = self.propagatesTo[key]

                # for each of them we check if removing connection removes it if it does we check continue going down
                for impact in impacts:
                    # -1 for node we are removing
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

            # If nodes relations already removed then cost his reduced
            cost = 0
            for propagator2 in self.contaminedBy[key]:
                if propagator2 in node.getCured():
                    cost -= 1

            cost += (len(self.contaminedBy[key])-K) + 1  # Cost to cure the person
            temp_list = node.getCured()
            total_impacts.extend(temp_list)
            # If Node produces a solution store it and continue
            if node.value - score < condition_success and node.cost + cost < bound:
                solution.append(Node(node.id + '1', total_impacts, node.value - score, node.cost + cost))
                bound = node.cost + cost
                if print_relation:
                    self.print_relation(keys, solution[-1], K)
                    continue
                print(str(bound) + '\n')
                continue

            # Else branch on Node to produce other Nodes 0 do nothing, 1 remove node
            Next_Node0 = Node(node.id + '0', node.cured, node.value, node.cost)
            Next_Node1 = Node(node.id + '1', total_impacts, node.value - score, node.cost + cost)

            # Check if produced Nodes bound can obtain optimal, if they can obtain optimal add them to queue
            # Two conditions to check:
            # Node already removed or end of possibility? This needs to be check after first level of contamination, and bound cost
            for new_node in [Next_Node0, Next_Node1]:
                if k == size_keys - 1 or k < size_keys - 1 and node.cured.count(keys[k+1]) == 1:
                    continue

            # if bound cost , note : python finishes execution if first condition fails
                if new_node.cost < bound:
                    # if len(solution) == 1:
                    #     queue.insert(0, new_node)  # Queue
                    #     continue
                    queue.append(new_node)  # Stack


    '''
    This function print the links that needs to be broken instead of the number of relation to be broken
    '''
    def print_relation(self, node, not_empty):

        # Open a file
        fo = open("results.txt", "a")

        if not_empty:
            print('\n')
            fo.write('\n')

        for link in node.getLinks():
            line = str(link[0]) + " " + str(link[1])
            print(line)
            fo.write(line + '\n')

        # Close opend file
        fo.close()