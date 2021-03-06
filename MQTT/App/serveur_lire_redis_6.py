'''
Fichier:	 python 3
Ecrit par :	 Tonow
Le :		 Date
Sujet:		 TODO
'''
import json
import ast
import redis
import csv
from datetime import datetime
import setting
import serveur_lire_csv_7

# dbname = input("choix de la db : ")
r = redis.StrictRedis()
list_retour = []
taille_prefix_topic = len(setting.defaut_base_topic_name)
entete_csv = ("Sortie","Date","Debit")

def read_message_from_server(msg_id, sortie_fichier):
    '''Lis tout le message contenue dans un id '''
    msg_id = str(msg_id) + '_id'
    dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
    for cle, valeur in dico_global_du_message.items():
        if setting.debug:
            print(f" cle : {cle} - valeur: {valeur}")
    if sortie_fichier:
        if setting.debug:
            print("desole pas de sortie fichier")

def read_all_message_from_server(sortie_fichier):
    '''Lis tout les messages contenue dans le server'''
    nb_cle = len(r.keys())
    # import pdb; pdb.set_trace()
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        read_dict = r.get(msg_id).decode("utf-8")
        read = read_dict[0] + "'" + read_dict[1:6] + "'" + read_dict[6] + "'" + read_dict[7:-31] + "'" + read_dict[-31:-30] + "'" + read_dict[-30:-26] + "'" + read_dict[-26:-25] + "'" + read_dict[-25:-1] + "'" + read_dict[-1:]
        dico_global_du_message = ast.literal_eval(read)
        for cle, valeur in dico_global_du_message.items():
            if setting.debug:
                print(f"{cle} : {valeur}")
            topic = msg_id
            debit = dico_global_du_message.get('debit')
            date = dico_global_du_message.get('date')
            import pdb; pdb.set_trace()
        list_retour.append((topic[taille_prefix_topic:],date,debit))
    if sortie_fichier:
        csv_ouput(list_retour)
    serveur_lire_csv_7.lire_csv_data()

def read_message_robinet_from_server(sortie_fichier):
    '''Lis tout le message contenue dans un d'un robinet '''
    list_sortie_eau = setting.list_sortie_eau()

    print("\nVoici la liste des sortie d'eau:")
    for sortie in list_sortie_eau:
        mot = sortie[0].split("_")
        text = " ".join(mot)
        print(f"{text} : {sortie[1]}")

    num_sortie = int(input("\nLa quelle voulez vous voir? : "))

    for sortie in list_sortie_eau:
        if num_sortie == sortie[1]:
            mot = sortie[0].split("_")
            topic_souhaiter = "/".join(mot)
            topic_souhaiter = setting.defaut_base_topic_name + topic_souhaiter

    if setting.debug:
        print(f"\nA la sortie {topic_souhaiter} :")
    nb_cle = len(r.keys())
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            if (cle == 'topic') and (valeur == topic_souhaiter):
                debit = dico_global_du_message.get('debit')
                date = dico_global_du_message.get('date')
                list_retour.append((valeur[taille_prefix_topic:],date,debit))
                if setting.debug:
                    print(f"\tdate : {date}\n\tdebit : {debit}")

    if sortie_fichier:
        csv_ouput(list_retour, topic_souhaiter)

def read_message_piece_from_server(sortie_fichier):
    '''Lis tout le message contenue dans un d'une piece '''
    list_sortie_eau = setting.list_sortie_eau()

    print("\nVoici la liste des sortie d'eau:")
    for sortie in list_sortie_eau:
        mot = sortie[0].split("_")
        text = " ".join(mot)
        print(f"{text} : {sortie[1]}")

    piece = input("\nQuelle piece voulez vous voir? : ")

    topic_souhaiter = setting.defaut_base_topic_name + piece

    if setting.debug:
        print(f"\nA la sortie {topic_souhaiter} :")
    nb_cle = len(r.keys())
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            if (cle == 'topic') and valeur.startswith(topic_souhaiter):
                longueur_char = len(topic_souhaiter)+1
                sortie_eau = " ".join(valeur[longueur_char:].split("/"))
                debit = dico_global_du_message.get('debit')
                date = dico_global_du_message.get('date')
                list_retour.append((valeur[taille_prefix_topic:],date,debit))
                if setting.debug:
                    print(f"sortie : {sortie_eau}\n\tdate : {date}\n\tdebit : {debit}")

    if sortie_fichier:
        csv_ouput(list_retour, topic_souhaiter)

def csv_ouput(list_retour, topic_souhaiter = "Debit_All_data_"+ str(datetime.now().date())):
    nom_fichier = 'Debit_' + "_".join(topic_souhaiter.split("/"))
    with open(nom_fichier + '.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(entete_csv)
        for item in list_retour:
            ligne = (item[0], item[1], item[2])
            writer.writerow(ligne)

def sortie_rapport():
    if setting.debug:
        # Tout les message    code : T
        # Un seul ligne       code : Id
        # Un seul robinet     code : R
        # Une seul piece      code : P
        text_choix = "Tout les message    code : T\nUn seul ligne       code : Id\nUn seul robinet     code : R\nUne seul piece      code : P\nSortie fichier      code + f : "

        sortie_fichier = False
        choix = input(text_choix)
        if choix.lower()[-1] == "f":
            sortie_fichier = True
        if choix.lower()[0] == "t":
            read_all_message_from_server(sortie_fichier)
        elif choix.lower()[0:1] == "id":
            msg_id = input("Tapez l'id : ")
            read_message_from_server(msg_id, sortie_fichier)
        elif choix.lower()[0] == "r":
            read_message_robinet_from_server(sortie_fichier)
        elif choix.lower()[0] == "p":
            read_message_piece_from_server(sortie_fichier)

    else:
        sortie_fichier = True
        read_all_message_from_server(sortie_fichier)
