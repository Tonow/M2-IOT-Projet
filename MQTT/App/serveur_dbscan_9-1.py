# -*- coding: utf-8 -*-
"""
===========================
DBSCAN clustering algorithm
===========================

Finds core samples of high density and expands clusters from them.

"""
print(__doc__)

import os

import time
import progressbar

import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

import setting
import serveur_envoi_mail_10

cluster_anormal = False



def propose_fichier_csv():
    if setting.debug:
        for file in os.listdir('.'):
            if file.endswith(".csv") and file.startswith("V"):
                print(file)

    if setting.debug:
        ficher_a_traiter = input("\nNom du fichier a traiter : ")
    else:
        ficher_a_traiter = "Debit_All_data_2018-03-16.csv"
    df = pd.read_csv(ficher_a_traiter)
    df.columns = ['Sortie',
              'Date',
              'Delta temps',
              'Volume'
              ,]
    return ficher_a_traiter

ficher_a_traiter = propose_fichier_csv()


dataframe = pd.read_csv(ficher_a_traiter)

if setting.debug:
    i = 0
    for col in dataframe.columns:
        print(f'colonne {i}: {col}')
        i = i+1


df = pd.read_csv(ficher_a_traiter)

dic_lite_sortie = dict(setting.list_sortie_eau)

labels_true = []
for line in df['Sortie']:
    line = dic_lite_sortie.get("_".join(line.split("/")))
    labels_true.append(line)
# df = pd.read_csv(ficher_a_traiter, dtype={'Sortie': 'category'}).dtypes
col_utile = df.as_matrix(columns=['Delta temps', 'Volume'])
# col_utile = df.as_matrix(columns=[df.columns[3], df.columns[4]])

df.columns = ['Sortie',
              'Date',
              'Delta temps',
              'Volume',]

X = col_utile

# #############################################################################
# Generate sample data

# #############################################################################
# Compute DBSCAN

eps_max_value = 300
eps_min_value = 1
eps_step = 2
min_samples_max_value = 20
min_samples_min_value = 1

if setting.debug:
    changement_val_defaut = input(f'\n\n Valeur par defaut\n \n eps_max_value: {eps_max_value} \n eps_min_value: {eps_min_value} \n eps_step: {eps_step} \n min_samples_max_value: {min_samples_max_value} \n min_samples_min_value: {min_samples_min_value} \n Voulez vous changer ces valeur? y/n : ')
    if changement_val_defaut.lower() == 'y':
        eps_max_value = float(input('votre eps_max_value ? : '))
        eps_min_value = float(input('votre eps_min_value  ? : '))
        eps_step = float(input('votre eps_step ? : '))
        min_samples_max_value = int(input('votre min_samples_max_value ? : '))
        min_samples_min_value = int(input('votre min_samples_min_value ? : '))


def db_scan(X, labels_true):
    best_adjusted_rand_index = 0
    best_v_measure_score = 0
    with progressbar.ProgressBar(max_value=eps_max_value) as bar:
        for eps in np.arange(eps_min_value, eps_max_value, eps_step):
            bar.update(eps)
            for min_samples in range(min_samples_min_value, min_samples_max_value):
                # print(f"esp: {eps}  |  min point {min_samples}")
                # db = DBSCAN(eps=0.3, min_samples=10).fit(X)
                db = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
                # import pdb; pdb.set_trace()

                # labels = DBSCAN().fit_predict(X)
                core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
                core_samples_mask[db.core_sample_indices_] = True
                labels = db.labels_

                # Number of clusters in labels, ignoring noise if present.
                n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

                adjusted_rand_index = metrics.adjusted_rand_score(labels_true, labels)
                v_measure_score = metrics.v_measure_score(labels_true, labels)
                best_adjusted_index = adjusted_rand_index > best_adjusted_rand_index
                best_v_measure = v_measure_score > best_v_measure_score
                if best_adjusted_index and best_v_measure:
                    if setting.debug:
                        print("#"*30)
                        print(f"esp: {round(eps, 3)}  |  min point {min_samples}")
                        # print("Adjusted Rand Index: %0.3f"
                        #       % metrics.adjusted_rand_score(labels_true, labels))
                        print(f"Adjusted Rand Index: {round(adjusted_rand_index, 3)}")
                        print(f"V-measure: {round(v_measure_score, 3)}")
                    best_labels = labels
                    best_core_samples_mask = core_samples_mask
                    best_n_clusters_ = n_clusters_
                    best_adjusted_rand_index = adjusted_rand_index
                    best_v_measure_score = v_measure_score
                    best_eps = eps
                    best_min_samples = min_samples

                    homogeneity = metrics.homogeneity_score(labels_true, labels)
                    completeness = metrics.completeness_score(labels_true, labels)

                    adjusted_mutual_information = metrics.adjusted_mutual_info_score(labels_true, labels)
                    silhouette_coefficient = metrics.silhouette_score(X, labels)

    if setting.debug:
        print("#"*50 +"\n")
        print("#"*15 + "  Rapport:  " + "#"*15 + "\n")
        print(f"Nombre de clusters estimer: {best_n_clusters_}")
        print(f"esp: {round(best_eps, 3)}  |  min point {best_min_samples} \n")
        print(f"Homogeneity: {round(homogeneity, 3)}")
        print(f"Completeness: {round(completeness, 3)}")
        print(f"Adjusted Mutual Information: {round(adjusted_mutual_information, 3)}")
        print(f"Silhouette Coefficient: {round(silhouette_coefficient, 3)}")
        print(f"Adjusted Rand Index: {round(best_adjusted_rand_index, 3)}")
        print(f"V-measure: {round(best_v_measure_score, 3)}")
        print("#"*50 +"\n")
    return (best_labels, best_core_samples_mask, best_n_clusters_)

(labels, core_samples_mask, n_clusters_) = db_scan(X, labels_true)

# #############################################################################
# Plot result
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
unique, counts = np.unique(labels, return_counts=True)
nb_val_in_cluster = dict(zip(unique, counts))

nb_cluster_anormaux = 0
for cluster, nombre_element in nb_val_in_cluster.items():
    if cluster == -1:
        cluster = 'noise'
    elif nombre_element == 1:
        cluster_anormal = True
        nb_cluster_anormaux = nb_cluster_anormaux + 1
        msg_ann = f" il y a {nb_cluster_anormaux} cluster(s) qui semble anormal(aux)"
    else:
        if setting.debug:
            print(f" Le cluster {cluster} a {nombre_element} element")

if setting.debug:
    if cluster_anormal:
            print(msg_ann)

if cluster_anormal:
    message_mail = "Bonjour,\nIl pourrait sembler qu'il y ai une consomation anormal"
else:
    message_mail = "Bonjour,\nTout semble normal dans votre consomation"

colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]

fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
ax = fig.add_subplot(111)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Noir pour noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

# deux colonne
    xy = X[class_member_mask & core_samples_mask]
    ax.scatter(xy[:, 0], xy[:, 1],  c=tuple(col), marker='o')

    xy = X[class_member_mask & ~core_samples_mask]
    ax.scatter(xy[:, 0], xy[:, 1],c=tuple(col), marker='+', s=180)


plt.title('Les differante classe trouver sont au nombre de : %d' % n_clusters_)
plt.savefig("volume_classification_db-scan_cluster.png", dpi = setting.dpi)
if setting.debug:
    plt.show()

serveur_envoi_mail_10.envoi_mail(message_mail)
