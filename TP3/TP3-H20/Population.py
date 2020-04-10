# coding=utf8
import numpy as np

class Population:
    # Contructeur for the graph
    EXEMPLAIRE_FOLDER = 'exemplaires/'

    def __init__(self, exemplaire):
        self.exemplaire = exemplaire
        self.data = None
        self.infected_person = None
        self.size = None
        self.nb_infections = None
        self.relations = None
        self.level_graph = None
        self.ContaminedBy = None

    # Process txt file data
    def load_exemplaire(self):
        self.size, self.nb_infections = np.loadtxt(Population.EXEMPLAIRE_FOLDER + self.exemplaire, delimiter=' ', max_rows=1, dtype=int, unpack=True)
        self.data = np.loadtxt(Population.EXEMPLAIRE_FOLDER + self.exemplaire, skiprows=1, max_rows=self.size, dtype=bool)
        self.infected_person = np.loadtxt(Population.EXEMPLAIRE_FOLDER + self.exemplaire, skiprows=self.size+1, max_rows=1, dtype=int)

    # Build relation dictionnary for Graph
    def buildRelation(self):
        g = dict.fromkeys(range(self.size))
        for i in range(self.size):
            relations = []
            for y in range(self.size):
                if self.data[i][y] == True:
                    relations.append(y)
            g[i] = relations
        self.relations = g

    # This iterate on the population to know each round who his infected and by whom
    def propagateInfection(self, K):
        infected = self.getInfectedPersons().copy().tolist()
        level = 0
        self.level_graph = {level: infected}
        # self.graph_propagators = {-1: infected} # Si l'on veut ajouter root a deja contamine
        self.ContaminedBy = {}

        while True:
            new_infected = []
            # Iteration on all population
            for i in range(self.size):
                who_infected_me = [] # To know how many infected an infected person has
                nb_relation_with_infected = 0 # Initialize the number of relation

                # Verifies if already infected
                if i not in infected:
                    for y in infected:
                        if self.data[i][y]:
                            who_infected_me.append(y)
                            nb_relation_with_infected += 1
                    if nb_relation_with_infected >= K:
                        new_infected.append(i)
                        self.ContaminedBy.update({i: who_infected_me})

            # Add new infected to list or get out
            if len(new_infected) == 0:
                return len(infected)
            else:
                level += 1
                self.level_graph.update({level: new_infected})
                infected = np.append(infected, np.array(new_infected))

    # Getters
    def getData(self):
        return self.data

    def getSize(self):
        return self.size

    def getInfectedPersons(self):
        return self.infected_person

    def getRelations(self):
        return self.relations

    def getLevelGraph(self):
        return self.level_graph

    def getContaminedBy(self):
        return self.ContaminedBy
