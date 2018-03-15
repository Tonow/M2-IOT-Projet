import json
import redis
import ast

import serveur_publish_data


def write_topic_json(payload, topic):
    data = {id_ring : {'topic': payload}}
    with open("sortie.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


dico = dict()

r = redis.StrictRedis(db = 1)
dico_global_du_message = ast.literal_eval((r.get(1)).decode("utf-8"))
for cle, valeur in dico_global_du_message.items():
    print(f"cle {cle} : valeur {valeur}")

    for clev, valeurv in valeur.items():
        if clev != "submit":
            print(f"clev {clev} : valeurv {valeurv}")
            dico.update({clev : valeurv})

data = {}
id_ring = 1
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

print("data")
print(data)

data_json = json.dumps(data, separators=(',', ':'))

serveur_publish_data.publish_data('new/topics', data_json)
with open("sortie.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
