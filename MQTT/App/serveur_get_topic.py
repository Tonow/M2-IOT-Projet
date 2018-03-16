import json
import redis
import ast

import setting
import serveur_publish_data


def write_topic_json(payload, topic):
    data = {id_ring : {'topic': payload}}
    with open("sortie.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


dico = dict()

r = redis.StrictRedis(db = 1)

nb_cle = len(r.keys())
for line_id in range(1, nb_cle):
    msg_id = "rings" + str(line_id)
    try:
        dico_global_du_message = ast.literal_eval((r.get(msg_id)).decode("utf-8"))
        for cle, valeur in dico_global_du_message.items():
            if setting.debug:
                print(f"cle {cle} : valeur {valeur}")

                for clev, valeurv in valeur.items():
                    if clev != "submit":
                        if setting.debug:
                            print(f"clev {clev} : valeurv {valeurv}")
                            dico.update({clev : valeurv})
    except:
        pass

data = {}
id_ring = 1
if setting.debug:
    print(dico)

for iteration in range(int(len(dico)/4)):
    i = iteration + 1
    for cle, valeur in dico.items():
        if valeur.endswith(str(i)):
            floor = dico.get("floor" + str(i))
            room = dico.get("room" + str(i))
            canalisation = dico.get("canalisation" + str(i))
            ringId =  dico.get("ringId" + str(i))
            num_output_longueur = len(ringId)
            while num_output_longueur != 4:
                ringId = "0" + ringId
                num_output_longueur = len(ringId)
            topic = floor + '/' + room + '/' + canalisation
            dico_topic = {ringId : {'topic': topic}}
        data.update(dico_topic)

if setting.debug:
    print("data")
    print(data)

data_json = json.dumps(data, separators=(',', ':'))

r.flushall()

serveur_publish_data.publish_data('new/topics', data_json)
with open("sortie.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
