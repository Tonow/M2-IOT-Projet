import paho.mqtt.publish as publish
import setting

topic = 'paho/test/topic'

default_topic = input(f"Topic par defaut: {topic} y/n ")
if default_topic.lower() == 'n':
    topic = input("Tapez le chemin du topic : ")

message = input("Tapez le message : ")

print(f"hotname = {setting.hostname}")

publish.single(topic, message, hostname=setting.hostname, qos=0, retain=False)
