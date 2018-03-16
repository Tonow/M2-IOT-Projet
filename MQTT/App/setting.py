# Differents settings globaux
import json

# hostname = "13.95.88.89"

hostname = "localhost"

# list_sortie_eau = [
#     ("SDB_lavabo_1", 0),
#     ("SDB_douche_1", 1),
#     ("SDB_machine_linge_1", 2),
#     ("Cuisine_evier_1", 3),
#     ("Cuisine_evier_1", 4),
#     ("Toilette_1", 5),
#     ("Toilette_60", 60),
# ]

defaut_base_topic_name = 'Company/home/bagues'

taille_prefix_topic = len(defaut_base_topic_name)
def list_sortie_eau(file_name = "sortie.json"):
    """ Lis un fichier json """
    with open(file_name) as json_data:
        data_from_file = json.load(json_data)
    for key, value in data_from_file.iteritems():
        temp = ["_".join(value[taille_prefix_topic:].split("/")),int(key)]
        list_sortie_eau.append(temp)
    import pdb; pdb.set_trace()
    return list_sortie_eau


debit_max = 256

# debug = True
debug = False # TODO Attention bien changer tout les fichier et tout re-tester



dpi = 300

nom_entreprise = 'WatOur'

client = "thomas.nowicki@hotmail.fr"

volume_fichier_data_general = "Volume_All_data_2018-03-16.csv"

debit_fichier_data_general = "Debit_All_data_2018-03-16.csv"
