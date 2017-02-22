# RemoteEyes
Repository for remote monitoring project

To Do:

1. MQTT to InfluxDB:
   - Refer to this example. It has callback functions for On-MQTT-Connect and On-MQTT-Messages received.
     https://github.com/rub-a-dub-dub/mqtt-influxdb/blob/master/mqtt-influxdb.py
   - Use the public m2m.Eclipse.org MQTT broker for testing first.
   - Set up private MQTT broker later.     
   - The above example uses the InfluxDB Python client plugin. Refer to:
     http://influxdb-python.readthedocs.io/en/latest/api-documentation.html as well as
     example in https://github.com/tzewantp/remote_eyes/blob/master/gateway/influxapp/flux_test1.py.

2. Setting up of private broker:
   - Refer to the following link:
   
3. Setting up Chronograf for data visualisation:

4. Receiving of XBee messages on BeagleBone:
