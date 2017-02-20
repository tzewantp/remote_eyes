# This MQTT client writes to a pre-created ThingSpeak account

# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python
#
# Requirements:
# o Python MQTT Client: "pip install paho-mqtt"
# o PS Utilities: "pip install psutil"

import time
import paho.mqtt.publish as publish
import psutil

# ThingSpeak Channel Settings
channelID = "224072"
apiKey = "IV4RT30CC3SUUT6L"
mqttHost = "mqtt.thingspeak.com"

# Create topic string
topic = "channels/" + channelID + "/publish/" + apiKey

# Initial value
tempValue = 32.1

tTransport = "tcp"
tPort = 1883
tTLS = None

while True:

   # Get the system performance data
   cpuPercent = psutil.cpu_percent(interval=20)
   ramPercent = psutil.virtual_memory().percent

   tPayload = "field1=" + str(cpuPercent) + "&field2=" + str(ramPercent)
   print("CPU = ", cpuPercent, " RAM = ", ramPercent)

   try:
      publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

   except:
      print("Error publishing")
   
