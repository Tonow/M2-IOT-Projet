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
            if cle == 'message':
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


    nb_cle = len(r.keys())
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            if (cle == 'topic') and (valeur == topic_souhaiter):
                if cle == 'message':
                    dico_global_du_message.get('message')



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
    pass
