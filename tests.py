import random
import math
import sys
import time
import csv
import matplotlib.pyplot as pl
import numpy as np

from algos import loadMatrix
from algos import runStandardProduct
from algos import runStrassenProduct


#Ce fichier permet d'obtenir les graphes des tests sur les différentes implémentations



#Tracé de la courbe de puissance
def tracer_puissance(Nlist, T, algo):
    #On représente le logarithme (en base 2) du temps de calcul en fonction du logarithme de la taille des matrices (soit N)
    pl.plot(Nlist, np.log2(T))
    pl.xlabel("log(Taille matrice)")
    pl.ylabel("log(Temps de calcul')")
    pl.title("Puissance" + " (" + algo + ")")
    pl.show()

#Tracé de la courbe de rapport
def tracer_rapport(Nlist, T, algo):
    if(algo == "standard"):
        #Hypothèse sur la complexité de l'algorithme classique : cube de la taille de la matrice
        pl.plot([2**N for N in Nlist], [T[i]/2**(3*Nlist[i]) for i in range(len(Nlist))])
        pl.xlabel("Taille matrice")
        pl.ylabel("Temps/Taille au cube")

    else:
        #Hypothèse sur la complexité de l'algorithme classique : taille de la matrice puissance log2(7) (soit environ 2.81)
        pl.plot([2**N for N in Nlist], [T[i]/2**(2.81*Nlist[i]) for i in range(len(Nlist))])
        pl.xlabel("Taille matrice")
        pl.ylabel("Temps/Taille puissance 2.81")

    pl.title("Rapport" + " (" + algo + ")")
    pl.show()

#Tracé de la courbe de constante
def tracer_constantes(n,T,algo):
    if(algo == "standard"):
        pl.plot([2**(3*N) for N in Nlist], T)
        pl.xlabel("Taille au cube")

    else:
        pl.plot([2**(2.81*N) for N in Nlist], T)
        pl.xlabel("Taille puissance 2.81")

    pl.ylabel("Temps de calcul")
    pl.title("Constantes" + " (" + algo + ")")
    pl.show()



seuil = 0

Tstd=[]
Tstra=[]
Nlist = [n for n in range(1, 8)]

#Pour chaque taille de matrice
for N in Nlist:
    print("___" + str(N) + "___\n")
    meanDurationStd = 0.0
    meanDurationStra = 0.0

    #On considère 10 couples de matrices (A, B)
    for i in range(1, 6):
        A = loadMatrix("mat/ex_" + str(N) + "_" + str(i))
        for j in range(i+1, 6):
            B = loadMatrix("mat/ex_" + str(N) + "_" + str(j))

            #On calcule le produit A*B selon chaque méthode et on note le temps de calcul
            M, duration = runStandardProduct(A, B, N)
            print(M)
            print(duration, "\t")
            meanDurationStd += duration

            M, duration = runStrassenProduct(A, B, N, seuil)
            print(M)
            print(duration, "\t")
            meanDurationStra += duration

    #On conserve la moyenne des temps de calcul sur les 10 essais
    Tstd.append(meanDurationStd / 10)
    Tstra.append(meanDurationStra / 10)

#Affichage des graphes
tracer_puissance(Nlist, Tstd, "standard")
tracer_rapport(Nlist, Tstd, "standard")
tracer_constantes(Nlist, Tstd, "standard")

tracer_puissance(Nlist, Tstra, "strassen")
tracer_rapport(Nlist, Tstra, "strassen")
tracer_constantes(Nlist, Tstra, "strassen")


