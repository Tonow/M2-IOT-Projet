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

def read_message_from_server(msg_id):
    '''Lis tout le message contenue dans un id '''
    msg_id = str(msg_id) + '_id'
    r = redis.StrictRedis()
    dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
    for cle, valeur in dico_global_du_message.items():
        print(f" cle : {cle} - valeur: {valeur}")

def read_all_message_from_server():
    '''Lis tout les messages contenue dans le server'''
    r = redis.StrictRedis()
    nb_cle = len(r.keys())
    for line_id in range(1, nb_cle):
        msg_id = str(line_id) + '_id'
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            if cle == 'message':
                print(f"{cle} : {valeur}")

msg_id = 4

all_messages = input(f"Tout les message  y/n ")
if all_messages.lower() == 'n':
    default_id = input(f"Id par defaut: {msg_id} y/n ")
    if default_id.lower() == 'n':
        msg_id = input("Tapez l'id : ")
    read_message_from_server(msg_id)
else:
    read_all_message_from_server()
