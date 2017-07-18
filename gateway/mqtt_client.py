# This MQTT client writes to the public Eclipse broker at m2m.eclipse.org
# Reference: https://www.eclipse.org/paho/articles/talkingsmall/

import time
import paho.mqtt.client as mqtt

''' #define SIMPLE_CONNECT  True '''

def publish_msg(reading):
    #if SIMPLE_CONNECT is True:
        try:
            mqttc = mqtt.Client()
            print('Connecting ...')
            mqttc.connect("m2m.eclipse.org", 1883, 60)
            print('Connected: reading=%.2f' % reading)
            mqttc.publish("remote_eyes/sensor","%.2f" % reading);
            mqttc.disconnect()
        except Exception, e:
            print('Error in connecting' + e.message)
    #else:
    #    print('TODO: Connection with callback handling')
    
