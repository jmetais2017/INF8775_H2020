# coding=utf8
import numpy as np

class Population:
    # Contructeur pour le graph
    EXEMPLAIRE_FOLDER = 'exemplaires/'

    def __init__(self, exemplaire):
        self.exemplaire = exemplaire
        self.data = None
        self.infected_person = None
        self.size = None
        self.nb_infections = None
        self.relations = None
        self.level_graph = None

    # Traite les donnes
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

    # Pour savoir selon la situation actuelle combien sont infecter
    def propagateInfection(self, K):
        infected = self.getInfectedPersons().copy()
        level = 0
        level_graph = {level: infected.tolist()}
        while True:
            new_infected = []

            for i in range(self.size):
                nb_relation_with_infected = 0 # Initialise le nombre de relation avec infecter
                # On commence par verifier si dans les infecter
                if i not in infected:
                    for y in infected:
                        if self.data[i][y]:
                            nb_relation_with_infected += 1
                    if nb_relation_with_infected >= K:
                        new_infected.append(i)
            # add new infected to list or get out
            if len(new_infected) == 0:
                self.level_graph = level_graph
                return len(infected)
            else:
                level += 1
                level_graph.update({level: new_infected})
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
