import paho.mqtt.publish as publish
from datetime import datetime
import setting


def cree_data(id_bague, debit):
    '''Avec le topic et message et le temps'''
    time = datetime.now()
    time_now = (
        str(time.year) + '/' +
        str(time.month) + '/' +
        str(time.day) + '-' +
        str(time.hour) + ":" +
        str(time.minute) + ":" +
        str(time.second)
    )
    text = ''
    for sortie in setting.list_sortie_eau:
        if int(id_bague) == sortie[1]:
            mot = sortie[0].split("_")
            text = "/".join(mot)
    topic = setting.defaut_base_topic_name + text
    data = {'debit': debit, 'date': time_now}
    if setting.debug:
        print("\n")
        for cle, valeur in data.items():
            print(f"{cle} : {valeur}")
    return (topic, str(data))


def publish_data(id_bague, debit):
    (topic, data) = cree_data(id_bague, debit)
    publish.single(topic, data, hostname=setting.hostname, qos=0, retain=False)
    if setting.debug:
        print(f"hotname = {setting.hostname}")
        print(f"Publish\n topic : {topic}\n data : {data}")
