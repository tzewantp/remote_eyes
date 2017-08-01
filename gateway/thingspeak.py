# This MQTT client writes to a pre-created ThingSpeak account

# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python
#
# Requirements:
# o Python MQTT Client: "pip install paho-mqtt"
# o PS Utilities: "pip install psutil"

import time
import paho.mqtt.publish as publish
import logging

def publish_mqtt(sensorValue):
    # ThingSpeak Channel Settings
    channelID = "224072"
    apiKey = "IV4RT30CC3SUUT6L"
    mqttHost = "mqtt.thingspeak.com"

    # Create topic string
    topic = "channels/" + channelID + "/publish/" + apiKey

    # Connection type
    tTransport = "tcp"
    tPort = 1883
    tTLS = None

    tPayload = "field1=" + str(sensorValue) 

    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
        print("Sensor Value = %0.2f" % sensorValue)
    except:
        print("Error publishing")
        logging.info("Error in publishing to thingspeak")
   
