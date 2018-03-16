'''
Fichier:	 python 3
Ecrit par :	 Tonow
Le :		 Date
Sujet:		 TODO
'''
import redis
import ast


def mqtt_to_data(topic, payload):
    # transforme en dictionnaire
    data = ast.literal_eval(payload.decode("utf-8"))
    data['topic'] = topic
    return data


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


def mqtt_to_redis(topic, payload):
    '''
        En dur recupere le topic et le payload et
        le met dans la data base redis
    '''
    data = mqtt_to_data(topic, payload)
    push_to_redis(data)
