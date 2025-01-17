import random
import math
import sys
import time
import matplotlib.pyplot as pl
import numpy as np
from scipy import stats

# from algos import loadMatrix
# from algos import runStandardProduct
# from algos import runStrassenProduct

# Ce fichier permet d'obtenir les graphes d'analyse hybride sur les différentes implémentations
# Tracé de la courbe de puissance


def tracer_puissance(Nlist, T, algo):
    logSizes = np.log2(Nlist)
    logTimes = np.log2(T)

    # On représente le logarithme (en base 2) du temps de calcul en fonction du logarithme de la taille d'exemplaire
    pl.plot(logSizes, logTimes, label="mesures")

    # Calcul de régression linéaire pour calculer l'exposant de la complexité
    fit = np.polyfit(logSizes, logTimes, 1)
    pl.plot(logSizes, [fit[0] * N + fit[1]
                       for N in logSizes], label="régression")
    pl.legend()
    # pl.text(Nlist[0], np.log2(T[len(T) - 2]), "Régression linéaire : \ny = " + str(int(1000*fit[0]) / 1000) + "x + " + str(int(1000*fit[1]) / 1000))

    pl.xlabel("log(Taille matrice)")
    pl.ylabel("log(Temps de calcul en s)")
    pl.title("Puissance" + " (" + algo + ")")
    pl.show()


# Tracé de la courbe de rapport
def tracer_rapport(Nlist, T, algo):
    doigts = 5
    if algo == "glouton":
        # Hypothèse sur la complexité de l'algorithme glouton :
        pl.plot([N for N in Nlist], [T[i] / doigts * Nlist[i]
                                     for i in range(len(Nlist))])
        pl.xlabel("Taille matrice")
        pl.ylabel("Temps/Taille glouton")

    if(algo == "dynamique"):
        # Hypothèse sur la complexité de l'algorithme glouton :
        pl.plot([N for N in Nlist], [T[i] / doigts**2 * Nlist[i]
                                     for i in range(len(Nlist))])
        pl.xlabel("Taille matrice")
        pl.ylabel("Temps/Taille progDyn")

    else:
        maxIteration = 100
        # Hypothèse sur la complexité de l'algorithme classique : taille de la matrice puissance log2(7) (soit environ 2.81)
        pl.plot([N for N in Nlist], [T[i] / maxIteration * np.log2(Nlist[i])
                                     for i in range(len(Nlist))])
        pl.xlabel("Taille matrice")
        pl.ylabel("Temps/Taille recherche locale")

    pl.title("Rapport" + " (" + algo + ")")
    pl.show()


# Tracé de la courbe de constante
def tracer_constantes(Nlist, T, algo):
    doigts = 5
    if algo == "glouton":
        # Hypothèse sur la complexité de l'algorithme glouton :
        pl.plot([doigts * N for N in Nlist], [T[i]
                                              for i in range(len(Nlist))], label="test constante")
        pl.xlabel("Longueur de la mélodie Th.")
        pl.ylabel("Longueur de la mélodie Exp.")

        fit = np.polyfit([doigts * N for N in Nlist], T, 1)
        pl.plot([doigts * N for N in Nlist], [fit[0] * (doigts * N) + fit[1]
                                              for N in Nlist], label="régression")
        slope, intercept, r_value, p_value, std_err = stats.linregress([doigts * N for N in Nlist], [T[i]
                                                                                                     for i in range(len(Nlist))])

        pl.text(doigts * Nlist[0], int((T[len(T) - 1] - T[0]) / 2), "Régression linéaire : \ny = " + str(
            int(10000000 * fit[0]) / 10000000) + "x + " + str(int(1000 * fit[1]) / 1000) + "\nR^2 = " + str(round(r_value, 3)))

    if algo == "programmation dynamique":
        # Hypothèse sur la complexité de l'algorithme prog. Dyn. :
        pl.plot([doigts**2 * N for N in Nlist], [T[i]
                                                 for i in range(len(Nlist))], label="test constante")
        pl.xlabel("Longueur de la mélodie Th.")
        pl.ylabel("Longueur de la mélodie Exp.")

        fit = np.polyfit([doigts**2 * N for N in Nlist], T, 1)
        pl.plot([doigts**2 * N for N in Nlist], [fit[0] * (doigts**2 * N) + fit[1]
                                                 for N in Nlist], label="régression")
        slope, intercept, r_value, p_value, std_err = stats.linregress([doigts**2 * N for N in Nlist], [T[i]
                                                                                                        for i in range(len(Nlist))])
        pl.text(doigts**2 * Nlist[0], int((T[len(T) - 1] - T[0]) / 2), "Régression linéaire : \ny = " + str(
            int(10000000 * fit[0]) / 10000000) + "x + " + str(int(1000 * fit[1]) / 1000) + "\nR^2 = " + str(round(r_value, 3)))

    if algo == "recherche locale":
        # Hypothèse sur la complexité de l'algorithme prog. Dyn. :
        pl.plot([np.log2(N) * N for N in Nlist], [T[i]
                                                  for i in range(len(Nlist))], label="test constante")
        pl.xlabel("Longueur de la mélodie Th.")
        pl.ylabel("Longueur de la mélodie Exp.")

        fit = np.polyfit([np.log2(N) * N for N in Nlist], T, 1)
        pl.plot([np.log2(N) * N for N in Nlist], [fit[0] * (np.log2(N) * N) + fit[1]
                                                  for N in Nlist], label="régression")
        slope, intercept, r_value, p_value, std_err = stats.linregress([np.log2(N) * N for N in Nlist], [T[i]
                                                                                                         for i in range(len(Nlist))])
        pl.text(np.log2(Nlist[0]) * Nlist[0], int((T[len(T) - 1] - T[0]) / 2), "Régression linéaire : \ny = " + str(
            int(10000000 * fit[0]) / 10000000) + "x + " + str(int(1000 * fit[1]) / 1000) + "\nR^2 = " + str(round(r_value, 3)))

    pl.legend()

    pl.title("Constantes" + " (" + algo + ")")
    pl.show()


exSizes = [1000, 3000, 10000, 30000, 100000,
           300000, 1000000, 3000000, 6000000, 8000000]

Tglouton = [0.004651856422424316, 0.015369033813476563, 0.055006551742553714, 0.15770671367645264,
            0.4962428569793701, 1.6334518432617187, 5.604541373252869, 17.08093640804291, 35.273496413230895, 37.36063899993896]
TprogDyn = [0.06831727027893067, 0.21262147426605224, 0.723763394355774, 2.2346749544143676, 7.2352567434310915,
            23.45234618186951, 78.18098702430726, 240.38777577877045, 460.2183406352997, 532.8789279937744]
TlocalSearch = [0.007136917114257813, 0.019548797607421876, 0.06697454452514648, 0.19590392112731933,
                0.6172402858734131, 2.0217474937438964, 6.9279080629348755, 21.201788425445557, 42.8545264005661, 46.51673395633698]

Cglouton = [14822.3, 44940.0, 149478.1, 447871.5, 1489408.2,
            4471309.6, 14912770.1, 44695951.3, 89378685.6, 119166828.1]
CprogDyn = [7624.7, 23102.6, 76644.0, 229620.5, 766408.3,
            2297932.4, 7652883.9, 22975208.5, 45940313.4, 61215935.8]
ClocalSearch = [14670.4, 44792.6, 149356.2, 447747.3, 1489251.2,
                4471183.2, 14912654.3, 44695800.7, 89378573.4, 119166671.3]

# Affichage des graphes
# tracer_rapport(exSizes, Cglouton, "glouton")
# tracer_rapport(exSizes, CprogDyn, "programmation dynamique")
# tracer_rapport(exSizes, ClocalSearch, "recherche locale")

# Affichage des graphes
tracer_constantes(exSizes, Tglouton, "glouton")
tracer_constantes(exSizes, TprogDyn, "programmation dynamique")
tracer_constantes(exSizes, TlocalSearch, "recherche locale")
