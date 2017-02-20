# This MQTT client writes to a pre-created ThingSpeak account

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
   
