#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
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

# This shows an example of using the publish.multiple helper function.

import paho.mqtt.publish as publish

topic = 'paho/test/topic'

default_topic = input(f"Topic par defaut: {topic} y/n ")
if default_topic.lower() == 'n':
    topic = input("Tapez le chemin du topic : ")

message_1 = input("Tapez le message 1 : ")
message_2 = input("Tapez le message 2 : ")

msgs = [{'topic': topic, 'payload': message_1}, (topic, message_2, 0, False)]
# publish.multiple(msgs, hostname="test.mosquitto.org")
publish.multiple(msgs, hostname="localhost")
print("publish ok")
