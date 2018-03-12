import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.cbook as cbook

def propose_fichier_csv():
    for file in os.listdir('.'):
        if file.endswith(".csv") and file.startswith("V"):
            print(file)

    ficher_a_traiter = input("\nNom du fichier a traiter : ")
    df = pd.read_csv(ficher_a_traiter)
    df.columns = ['Sortie',
              'Date',
              'Delta temps',
              'Volume'
              ,]
    return ficher_a_traiter


def choix_colonne(ficher_a_traiter):
    with open(ficher_a_traiter, newline='') as f:
      reader = csv.reader(f)
      row1 = next(reader)
      id_colonne = 0
      for colonne in row1:
          print(f"{colonne} : id = {id_colonne}")
          id_colonne = id_colonne + 1
    choix_x = int(input("\nChoix de la colonne x : "))
    choix_y = int(input("\nChoix de la colonne y : "))
    return (choix_x, choix_y)


def plot_volume_temps(ficher_a_traiter, choix_x, choix_y):
    # fname = cbook.get_sample_data(ficher_a_traiter, asfileobj=False)

    plt.plotfile(ficher_a_traiter, cols=(choix_x, choix_y))
    plt.savefig(ficher_a_traiter[:-3] + ".png", dpi=72)
    plt.show()

ficher_a_traiter = propose_fichier_csv()
(choix_x, choix_y) = choix_colonne(ficher_a_traiter)

plot_volume_temps(ficher_a_traiter, choix_x, choix_y)
