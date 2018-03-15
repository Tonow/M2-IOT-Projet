import paho.mqtt.publish as publish
from datetime import datetime
import setting


def publish_data(topic, data):
    publish.single(topic, data, hostname=setting.hostname, qos=0, retain=False)
    if setting.debug:
        print(f"hotname = {setting.hostname}")
        print(f"Publish\n topic : {topic}\n data : {data}")
