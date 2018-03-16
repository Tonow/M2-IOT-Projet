import os
import csv
from csv import reader
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
import setting


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
    with open(ficher_a_traiter, 'r') as f:
        data = list(reader(f))

    data1 = []
    data2 = []
    for line in data:
        try:
            data1.append(float(line[choix_x]))
            data2.append(float(line[choix_y]))
        except:
            pass
    fig, ax = plt.subplots()
    ax.scatter(data1, data2, alpha=0.5)
    ax.set_ylabel('Volume', fontsize=15)
    ax.set_xlabel(r'$\Delta_{temps}$', fontsize=15)
    ax.set_title('Volume en fonction du delta temps')
    plt.savefig("volume_temps.png", dpi = setting.dpi)
    if setting.debug:
        plt.show()

def plot_volume_date(ficher_a_traiter, date, volume):
    with open(ficher_a_traiter, 'r') as f:
        data = list(reader(f))

    data_date = []
    data_volume = []
    for line in data:
        try:
            data_date.append(line[date])
            data_volume.append(float(line[volume]))
        except:
            pass
    fig, ax = plt.subplots()
    ax.scatter(data_date[1:], data_volume, alpha=0.5)
    ax.set_ylabel('Volume', fontsize=15)
    fig.autofmt_xdate()
    ax.set_xlabel(r'Date', fontsize=15)
    ax.set_title('Volume en fonction des jours')
    plt.savefig("volume_date.png", dpi = setting.dpi)
    if setting.debug:
        plt.show()


def plot_volume_ring(ficher_a_traiter, choix_x, choix_y):
    with open(ficher_a_traiter, 'r') as f:
        data = list(reader(f))
    # fname = cbook.get_sample_data(ficher_a_traiter, asfileobj=False)

    # plt.plotfile(ficher_a_traiter, cols=(choix_x, choix_y))
    # plt.plotfile(ficher_a_traiter, cols=(choix_x, choix_y))
    # plt.savefig(ficher_a_traiter[:-3] + "png", dpi = setting.dpi)
    data1 = []
    data2 = []
    for line in data:
        try:
            data1.append(line[choix_x])
            data2.append(float(line[choix_y]))
        except:
            pass

    Xuniques, X = np.unique(data1[1:], return_inverse=True)
    colors = [int(i % 23) for i in X]
    fig, ax = plt.subplots()
    ax.scatter(X, data2, c = colors , alpha=0.5)
    ax.xaxis.set_ticks(X)
    ax.xaxis.set_ticklabels(Xuniques)
    ax.set_ylabel('Volume', fontsize=15)
    fig.autofmt_xdate()
    ax.set_xlabel(r'Sortie', fontsize=15)
    ax.set_title('Volume en fonction de la sortie')
    plt.savefig("volume_ring.png", dpi = setting.dpi)
    if setting.debug:
        plt.show()


def plot_volume_temps_ring(ficher_a_traiter, choix_sortie, choix_volume, choix_delta_temps):
    with open(ficher_a_traiter, 'r') as f:
        data = list(reader(f))

    data_sortie = []
    data_delta_temps = []
    data_volume = []
    for line in data:
        try:
            data_sortie.append(line[choix_sortie])
            data_delta_temps.append(float(line[choix_delta_temps]))
            data_volume.append(float(line[choix_volume]))
        except:
            pass

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    Xuniques, X = np.unique(data_sortie[1:], return_inverse=True)

    colors = [int(i % 23) for i in X]

    ax.scatter(X, data_delta_temps, data_volume, c = colors)
    ax.xaxis.set_ticks(X)
    ax.xaxis.set_ticklabels(Xuniques)

    ax.set_xlabel('Sortie', fontsize=15)
    ax.set_ylabel(r'$\Delta_{temps}$', fontsize=15)
    ax.set_zlabel('Volume', fontsize=15)
    plt.title('Volume en fonction sortie et du Delta temps')
    plt.savefig("volume_temps_ring.png", dpi = setting.dpi)
    if setting.debug:
        plt.show()




if setting.debug:
    ficher_a_traiter = propose_fichier_csv()
    (choix_x, choix_y) = choix_colonne(ficher_a_traiter)
else:
    # ficher_a_traiter = "Debit_All_data_2018-03-16.csv"
    ficher_a_traiter = "Volume_All_data_2018-03-11.csv"
    choix_sortie = 0
    choix_date = 1
    choix_delta_temps = 2
    choix_volume = 3


plot_volume_temps(ficher_a_traiter, choix_delta_temps, choix_volume)

plot_volume_date(ficher_a_traiter, choix_date, choix_volume)

plot_volume_ring(ficher_a_traiter, choix_sortie, choix_volume)

plot_volume_temps_ring(ficher_a_traiter, choix_sortie, choix_volume, choix_delta_temps)
