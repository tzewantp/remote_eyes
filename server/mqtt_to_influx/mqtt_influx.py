#!/usr/bin/env python


import sys
import signal
from influxdb import InfluxDBClient
import json
import urllib
c
import paho.mqtt.client as mqtt
#import datetime
import time

# This lets the message received event handler know that the DB connection is ready
dbConn = None
# This is the MQTT client object
client = None

dbhost = 'localhost'
dbport = 8086
dbuser = 'root'
dbpwd = 'root'
dbname = 'myFirstDB'
dbseries = 'myFirstDB'
dbcolname = 'reading'
mqtthost ='m2m.eclipse.org'
mqttport = 1883
mqttuser = None
mqttpwd = None
mqttqos = 1
mqttclient = None
topic = 'remote_eyes/sensor'
logfile = None
v = 0

# For writing to InfluxDB
# TimeStamp:
#timestamp=datetime.datetime.utcnow().isoformat()
#timestamp = "2009-11-10T23:00:00Z"
# Station Name that is recording the measurement
station_name="S2"
  
def _sigIntHandler(signum, frame):
    '''This function handles Ctrl+C for graceful shutdown of the programme'''
    logging.info("Received Ctrl+C. Exiting.")
    stopMQTT()
    stopInfluxDB()
    exit(0)

def setupLogging():
    '''Sets up logging'''
    verbosityLevel = 5
    logging.basicConfig(level=verbosityLevel, format='%(asctime)s %(message)s')

def setupSigInt():
    '''Sets up our Ctrl + C handler'''
    signal.signal(signal.SIGINT, _sigIntHandler)
    logging.debug("Installed Ctrl+C handler.")

def _mqttOnConnect(client, userdata, flag, rc):
    '''This is the event handler for when one has connected to the MQTT broker. 
       Will exit() if connection is not successful.'''
    if rc == 0:
        logging.info("Connected to MQTT broker successfully.")
        client.subscribe(topic, qos=mqttqos)
        startInfluxDB()
        return
    elif rc == 1:
        logging.critical("Connection to broker refused - incorrect protocol version.")
    elif rc == 2:
        logging.critical("Connection to broker refused - invalid client identifier.")
    elif rc == 3:
        logging.critical("Connection to broker refused - server unavailable.")
    elif rc == 4:
        logging.critical("Connection to broker refused - bad username or password.")
    elif rc == 5:
        logging.critical("Connection to broker refused - not authorised.")
    elif rc >=6:
        logging.critical("Reserved code received!")
    
    client.close()
    exit(1)

def _mqttOnMessage(client, userdata, message):
    global dbConn
    '''This is the event handler for a received message from the MQTT broker.'''
    logging.debug("Received message: " + str(message.payload))
    print("message received  "  ,str(message.payload))

    if dbConn is not None:
        sendToDB(message.payload)
    else:
        logging.warning("InfluxDB connection not yet available. Received message dropped.")


def sendToDB(payload):
    '''This function will transmit the given payload to the InfluxDB server'''

    global dbConn
    #now = datetime.datetime.today()
    #now = datetime.datetime.utcnow()
    now = time.gmtime()
    pointValues = [
       {
          "time": time.strftime("%Y-%m-%d %H:%M:%S", now),
          "measurement": dbcolname,
          "tags": {
              "nodeId": "node_1",
          },
          "fields": {
              "value": payload
          }, 
       }
    ]
     
    try:
        dbConn.write_points(pointValues)
    
    except Exception, e:   
        try:
            logging.critical("Couldn't write to InfluxDB: " + e.message)
        except TypeError, e2:
            logging.critical("Couldn't write to InfluxDB.")


def startInfluxDB():
    '''This function sets up our InfluxDB connection'''
    global dbConn
    try:
        dbConn = InfluxDBClient(dbhost, dbport, dbuser, dbpwd, dbname)
        #dbConn.create_database(dbname)
        logging.info("Connected to InfluxDB.")
        print("Connected to InfluxDB.")
    except InfluxDBClientError as e:
        try:
            logging.critical("Could not connect to Influxdb. Message: " + e.content)
            stopMQTT()
            exit(1)
    	except:
            logging.critical("Could not connect to InfluxDB.")
	    print("Could not connect to InfluxDB.")
            stopMQTT()
            exit(1) 

def stopInfluxDB():
    '''This functions closes our InfluxDB connection'''
    dbConn = None
    logging.info("Disconnected from InfluxDB.") 
    print("Disconnected from InfluxDB.") 

def startMQTT():
    '''This function starts the MQTT connection and listens for messages'''
    global client
    
    if mqttclient is not None:
        client = mqtt.Client(mqttclient, clean_session=False)
    else:
        client = mqtt.Client()
    
    client.on_connect = _mqttOnConnect
    client.on_message = _mqttOnMessage
    
    if mqttuser is not None:
        client.username_pw_set(mqttuser, mqttpwd)
    
    client.connect(mqtthost, mqttport, 60)
     
def stopMQTT():
    '''This function stops the MQTT client service'''
    global client
    if client is not None:
        client.disconnect()
        logging.info("Disconnected from MQTT broker.")
        client = None
    else:
        logging.warning("Attempting to disconnect without first connecting to MQTT broker.")


def main():
    # Now setup logging
    setupLogging()

    # Setup interrupt handler
    setupSigInt()

    # Open a connection to MQTT server and subscribe
    startMQTT()

    # Stay here forever
    global client
    while True:
        client.loop()

    # Clean-up and exit if got here.
    stopInfluxDB()
    stopMQTT()

if __name__ == "__main__":
    main()
