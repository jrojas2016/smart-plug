#!/usr/bin/python

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

# import sys
# try:
#     import paho.mqtt.client as mqtt
# except ImportError:
#     # This part is only required to run the example from within the examples
#     # directory when the module itself is not installed.
#     #
#     # If you have the module installed, just use "import paho.mqtt.client"
#     import os
#     import inspect
#     cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
#     if cmd_subfolder not in sys.path:
#         sys.path.insert(0, cmd_subfolder)
#     import paho.mqtt.client as mqtt

import paho.mqtt.client as mqtt

mqttc = mqtt.Client()

#mqttc.username_pw_set('bmzrmflw', 'h7hmUII91mvS')
#mqttc.connect('m10.cloudmqtt.com', '11163')
mqttc.username_pw_set('iajmzgae', 'bNl5xzae8mox')
mqttc.connect("m12.cloudmqtt.com", 16186, 60)


# Publish a message
#mqttc.publish("SmartPlug", "{'command':'on'}")
#mqttc.publish("SmartPlugData", "{\"command\":\"On\"}")
mqttc.publish("SmartPlugData", "{\"timestamp\":\"0.0\",\"app_id\":\"0\",\"app_state\":\"off\",\"app_event\":\"turn_on\"}" )
