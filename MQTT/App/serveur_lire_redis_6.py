'''
Fichier:	 python 3
Ecrit par :	 Tonow
Le :		 Date
Sujet:		 TODO
'''
import json
import ast
import redis
from datetime import datetime
import setting

r = redis.StrictRedis()

def read_message_from_server(msg_id):
    '''Lis tout le message contenue dans un id '''
    msg_id = str(msg_id) + '_id'
    dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
    for cle, valeur in dico_global_du_message.items():
        print(f" cle : {cle} - valeur: {valeur}")

def read_all_message_from_server():
    '''Lis tout les messages contenue dans le server'''
    nb_cle = len(r.keys())
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            print(f"{cle} : {valeur}")

def read_message_robinet_from_server():
    '''Lis tout le message contenue dans un d'un robinet '''
    list_sortie_eau = setting.list_sortie_eau

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
                if setting.debug:
                    print(f"\tdate : {date}\n\tdebit : {debit}")


def read_message_piece_from_server():
    '''Lis tout le message contenue dans un d'une piece '''
    list_sortie_eau = setting.list_sortie_eau

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
                if setting.debug:
                    print(f"sortie : {sortie_eau}\n\tdate : {date}\n\tdebit : {debit}")

# Tout les message    code : T
# Un seul ligne       code : Id
# Un seul robinet     code : R
# Une seul piece      code : P
text_choix = "Tout les message    code : T\nUn seul ligne       code : Id\nUn seul robinet     code : R\nUne seul piece      code : P\n"


choix = input(text_choix)
if choix.lower() == "t":
    read_all_message_from_server()
elif choix.lower() == "id":
    msg_id = input("Tapez l'id : ")
    read_message_from_server(msg_id)
elif choix.lower() == "r":
    read_message_robinet_from_server()
elif choix.lower() == "p":
    read_message_piece_from_server()
