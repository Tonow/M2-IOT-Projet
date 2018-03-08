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
    r = redis.StrictRedis()
    dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
    for cle, valeur in dico_global_du_message.items():
        print(f" cle : {cle} - valeur: {valeur}")

msg_id = 4

default_id = input(f"Id par defaut: {msg_id} y/n ")
if default_id.lower() == 'n':
    msg_id = input("Tapez l'id : ")

msg_id = str(msg_id) + '_id'

read_message_from_server(msg_id)
