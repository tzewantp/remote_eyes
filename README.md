# RemoteEyes
Repository for remote monitoring project

To Do:

**1. MQTT to InfluxDB:**
   - Refer to this example. It has callback functions for On-MQTT-Connect and On-MQTT-Messages received.
     https://github.com/rub-a-dub-dub/mqtt-influxdb/blob/master/mqtt-influxdb.py
   - Use the public m2m.Eclipse.org MQTT broker for testing first.
   - Set up private MQTT broker later.     
   - The above example uses the InfluxDB Python client plugin. Refer to:
     http://influxdb-python.readthedocs.io/en/latest/api-documentation.html as well as
     example in https://github.com/tzewantp/remote_eyes/blob/master/gateway/influxapp/flux_test1.py.

**2. Setting up of private broker:**
   - Refer to the following link:
   
**3. Setting up Chronograf or Grafana for data visualisation:**

**4. Receiving of XBee messages on BeagleBone:**

**5. Writing the Pulse Generator** 
   - Write a simple serial terminal program (controlled from PC) to control how the hardware should respond to commands from the PC.
   - The following example uses the **mbed asynchronous APIs**:
     https://developer.mbed.org/teams/SiliconLabs/wiki/Using-the-mbed-asynchronous-APIs
     This API makes use of asynchronous event handling through the serial channel.
     Note: It is tested on the STM32F401RE board, but not yet on the STM32F042K6 board.
