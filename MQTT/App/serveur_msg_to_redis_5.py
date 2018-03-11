'''
Fichier:	 python 3
Ecrit par :	 Tonow
Le :		 Date
Sujet:		 TODO
'''
import json
import redis
from datetime import datetime


def write_topic_json(payload, topic):
    """ Prend un payloud et un topic et le met dans un json """
    time = datetime.now()
    time_now = (
        str(time.year) + '/' +
        str(time.month) + '/' +
        str(time.day) + '-' +
        str(time.hour) + ":" +
        str(time.minute) + ":" +
        str(time.second)
    )
    # data = {'data': [{'topic': topic, 'message': payload, 'date': time_now}]}
    data = {'topic': topic, 'message': payload, 'date': time_now}
    with open("sortie.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def read_json_file(file_name):
    """ Lis un fichier json """
    with open(file_name) as json_data:
        data_from_file = json.load(json_data)
    return data_from_file


def push_to_redis(data):
    """ Met un json dans un db redis """
    # pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.StrictRedis()

    # donne un nom incrementer adans la db redis
    id_data = str(r.incr('id_data')) + "_id"

    # set la data au bon nom
    r.set(id_data, data)

    cle = r.keys()
    print(f"les cle sont : {cle}")


def file_json_to_redis():
    """ En dur recupere le fichier json et le met dans la data base redis """
    data = read_json_file('sortie.json')
    push_to_redis(data)
