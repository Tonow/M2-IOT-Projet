#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

import paho.mqtt.client as mqtt
import to_server
import setting


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print('#'*30 + '\n' + '#'*30)
    print("Voici un nouveau message !")
    print(f"topic: {msg.topic}  qos: {str(msg.qos)}  msg: {str(msg.payload)}")
    to_server.write_topic_json(str(msg.payload), str(msg.topic))
    to_server.file_json_to_redis()


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


default_topic = input("Topic par defaut? y/n ")
if default_topic.lower() == 'n':
    topic = input("Tapez le chemin du topic : ")
else:
    topic = 'paho/test/topic'
    print(f"le topic : {topic}")

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
# mqttc.connect(host="test.mosquitto.org", port=1883, keepalive=60, bind_address="")
mqttc.connect(host=setting.hostname, port=1883, keepalive=60, bind_address="")
# mqttc.connect("m2m.eclipse.org", 1883, 60)
# mqttc.subscribe("$SYS/#", 0)
mqttc.subscribe(topic + "/#", 0)

mqttc.loop_forever()
