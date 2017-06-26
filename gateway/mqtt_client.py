# This MQTT client writes to the public Eclipse broker at m2m.eclipse.org
# Reference: https://www.eclipse.org/paho/articles/talkingsmall/

import time
import paho.mqtt.client as mqtt

def publish_msg(reading):
    mqttc = mqtt.Client()
    mqttc.connect("m2m.eclipse.org", 1883, 60)
    print('reading=%.2f' % reading)
    mqttc.publish("remote_eyes/sensor","%.2f" % reading);
    mqttc.disconnect()
     