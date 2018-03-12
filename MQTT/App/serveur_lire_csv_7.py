import csv
import os
import re
import setting
from datetime import datetime

cwd = os.getcwd()
entete_csv = ("Sortie", "Date", "Delta temps", "Volume")
list_retour = []
date_precedante = False
debit_precedant = 0
volume_precedant = 0
somme_volume = 0

def propose_fichier_csv():
    for file in os.listdir('.'):
        if file.endswith(".csv"):
            print(file)

    ficher_a_traiter = input("\nNom du fichier a traiter : ")
    return ficher_a_traiter

def calcule_volumes_consomation_eau(ficher_a_traiter, date_precedante = False, debit_precedant = 0, volume_precedant = 0, somme_volume = 0):
    with open(ficher_a_traiter, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            topic = row[0]
            date = row[1]
            debit = row[2]

            # Evite la premiere ligne ou sont ecrite les nom des colonnes
            if len(date) > 4:
                date_format = datetime.strptime(date, "%Y/%m/%d-%H:%M:%S")

                if debit == 0 or not date_precedante:
                    date_precedante = date_format
                    delta_temps = 0
                    volume = 0
                else:
                    delta_temps = (date_format - date_precedante).total_seconds()
                    volume = delta_temps * float(debit_precedant)
                    somme_volume = somme_volume + volume

                volume_precedant = volume
                debit_precedant = debit

                if setting.debug:
                    print(f"{debit} : {delta_temps} : {volume} : {somme_volume}")

            if debit == "0":
                list_retour.append((topic,date_format,delta_temps,somme_volume))
                if setting.debug:
                    print(f"{topic} : {date_format} : {debit} : {delta_temps} : {volume} : {somme_volume}")
                date_precedante = False
                volume_precedant = 0
                somme_volume = 0
    csv_ouput(list_retour, ficher_a_traiter)

def csv_ouput(list_retour, nom_fichier):
    with open('Volume' + nom_fichier[5:], 'w') as f:
        writer = csv.writer(f)
        writer.writerow(entete_csv)
        for item in list_retour:
            ligne = (item[0], item[1], item[2], item[3])
            writer.writerow(ligne)

ficher_a_traiter = propose_fichier_csv()
calcule_volumes_consomation_eau(ficher_a_traiter)
