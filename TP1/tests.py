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
    pl.plot(Nlist, np.log2(T), label = "mesures")

    fit = np.polyfit(Nlist, np.log2(T), 1)
    pl.plot(Nlist, [fit[0]*N + fit[1] for N in Nlist], label = "régression")
    pl.legend()
    pl.text(Nlist[0], np.log2(T[len(T) - 2]), "Régression linéaire : \ny = " + str(int(1000*fit[0]) / 1000) + "x + " + str(int(1000*fit[1]) / 1000))

    pl.xlabel("log(Taille matrice)")
    pl.ylabel("log(Temps de calcul en s)")
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
        pl.plot([2**(3*N) for N in Nlist], T, label = "mesures")
        pl.xlabel("Taille au cube")
        fit = np.polyfit([2**(3*N) for N in Nlist], T, 1)
        pl.plot([2**(3*N) for N in Nlist], [fit[0]*(2**(3*N)) + fit[1] for N in Nlist], label = "régression")

    else:
        pl.plot([2**(2.81*N) for N in Nlist], T, label = "mesures")
        pl.xlabel("Taille puissance 2.81")
        fit = np.polyfit([2**(2.81*N) for N in Nlist], T, 1)
        pl.plot([2**(2.81*N) for N in Nlist], [fit[0]*(2**(2.81*N)) + fit[1] for N in Nlist], label = "régression")

    pl.legend()
    pl.text(2**(3*Nlist[0]), T[len(T) - 2], "Régression linéaire : \ny = " + str(int(10000000*fit[0]) / 10000000) + "x + " + str(int(1000*fit[1]) / 1000))

    pl.ylabel("Temps de calcul en s")
    pl.title("Constantes" + " (" + algo + ")")
    pl.show()



seuil = 3

Tstd=[]
Tstra=[]
Nlist = [n for n in range(1, 10)]

# #Pour chaque taille de matrice
# for N in Nlist:
#     print("___" + str(N) + "___\n")
#     meanDurationStd = 0.0
#     meanDurationStra = 0.0
#
#     #On considère 10 couples de matrices (A, B)
#     for i in range(1, 6):
#         A = loadMatrix("mat/ex_" + str(N) + "_" + str(i))
#         for j in range(i+1, 6):
#             B = loadMatrix("mat/ex_" + str(N) + "_" + str(j))
#
#             #On calcule le produit A*B selon chaque méthode et on note le temps de calcul
#             M, duration = runStandardProduct(A, B, N)
#             print(M)
#             print(duration, "\t")
#             meanDurationStd += duration
#
#             M, duration = runStrassenProduct(A, B, N, seuil)
#             print(M)
#             print(duration, "\t")
#             meanDurationStra += duration
#
#     #On conserve la moyenne des temps de calcul sur les 10 essais
#     Tstd.append(meanDurationStd / 10)
#     Tstra.append(meanDurationStra / 10)
#
# print(Tstd)
# print(Tstra)

Tstd = [0.0, 0.0, 0.0, 0.003777337074279785, 0.03255352973937988, 0.20620810985565186, 1.5496347188949584, 12.515714097023011, 107.4036092042923]
Tstra = [0.0, 0.0, 0.0022002458572387695, 0.01938738822937012, 0.14595155715942382, 0.7966845750808715, 5.48813910484314, 39.286847138404845, 278.8520452022552]
Tstra2 = [0.0, 0.0002938508987426758, 0.0006030321121215821, 0.004490089416503906, 0.02523086071014404, 0.17273094654083251, 1.185133123397827]
Tstra3 = [0.00020089149475097657, 0.00010023117065429687, 0.0006011009216308593, 0.0032975196838378905, 0.022534799575805665, 0.15149009227752686, 1.0528615951538085, 7.704970598220825, 52.32933306694031]
Tsra4 = [0.0, 0.0, 0.0005008459091186523, 0.0035990476608276367, 0.02333648204803467, 0.15950314998626708, 1.1221461296081543]
Tsra5 = [0.0, 9.95635986328125e-05, 0.0003958463668823242, 0.0035883903503417967, 0.027031254768371583, 0.19508640766143798, 1.2908326625823974]


#Affichage des graphes
tracer_puissance(Nlist[3:10], Tstd[3:10], "standard")
tracer_rapport(Nlist, Tstd, "standard")
tracer_constantes(Nlist, Tstd, "standard")


tracer_puissance(Nlist[3:10], Tstra[3:10], "strassen")
tracer_rapport(Nlist, Tstra, "strassen")
tracer_constantes(Nlist, Tstra, "strassen")


tracer_puissance(Nlist[3:10], Tstra3[3:10], "strassen, seuil = 3")
tracer_rapport(Nlist, Tstra3, "strassen, seuil = 3")
tracer_constantes(Nlist, Tstra3, "strassen, seuil = 3")


