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

import apscheduler.schedulers.background as bg
import paho.mqtt.client as mqtt # MQTT protocol interface
from pymongo import MongoClient #DB interface
import multiprocessing as mp
import flask as fl
import logging
import urllib2
import time
import json
import sys
import os
sys.path.append(os.getcwd())

app = fl.Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

log = logging.getLogger('apscheduler.executors.default')
log2 = logging.getLogger('apscheduler.scheduler')
log.setLevel(logging.INFO)  #DEBUG
log2.setLevel(logging.INFO) #DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
log2.addHandler(h)

# HOST_URL = 'http://localhost:5000/'	#Local use only
HOST_URL = 'http://smart-plug.herokuapp.com/'

'''Utilities'''
def curl( url, data = None, authToken = None ):

	if data is not None:
		req = urllib2.Request( url, data )
	else:
		req = urllib2.Request( url )

	if authToken is not None:
		req.add_header( 'Authorization', 'Basic %s'%authToken )

	response = urllib2.urlopen( req )
	res = response.read()
	return res

def getDb():
	print "Connecting to DB."
	mongo_client = MongoClient('mongodb://heroku_p72xffsz:nnhjpmb6hhu0kuf5eojdhrsp8k@ds145315.mlab.com:45315/heroku_p72xffsz')
	db = mongo_client['heroku_p72xffsz']
	collection = db['data']
	# mongo_client = MongoClient()  #Local use only
	# db = mongo_client['serial-plug-data']
	# collection = db['data']

	return collection

'''MQTT'''
def on_connect(mqttc, obj, flags, rc):
	print("rc: "+str(rc))

def on_log(mqttc, obj, level, string):
	print(string)

def on_subscribe(mqttc, obj, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(mqttc, obj, mid):
	print("mid: "+str(mid))

def on_message(mqttc, obj, msg):
	print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

	collection = getDb()
	# dbConnection = sqlite3.connect("C:\Users\Robotics.Phd\.ssh\Documents\DataBases\SmartPlugData.db")
	# dbCursor = dbConnection.cursor()

	# Get timestamp in EPOCH/UTC
	sTime = time.time() # Seconds since EPOCH
	sTimeStamp = (sTime,) # To avoid HACKERS

	# Insert a row of data
	# dbCursor.execute("INSERT INTO rawData VALUES (?,'0','on','turn_on','120.0','1.0','120.0','0','off','turn_on')", sTimeStamp)
	# Save (commit) the changes
	# dbConnection.commit()
	payload = json.loads(msg.payload)
	payload['timestamp'] = sTimeStamp
	collection.insert_one(payload)
	print "Data saved to DB!"

	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	# dbConnection.close()

'''FLASK'''
@app.before_first_request
def setupScheduler(*args, **kwargs):
	sched = bg.BackgroundScheduler()

	# If you want to use a specific client id, use
	# mqttc = mqtt.Client("client-id")
	# but note that the client id must be unique on the broker. Leaving the client
	# id parameter empty will generate a random id for you.
	mqttc = mqtt.Client()
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.on_subscribe = on_subscribe
	# Uncomment to enable debug messages
	# mqttc.on_log = on_log
	# mqttc.connect("m2m.eclipse.org", 1883, 60)
	# mqttc.subscribe("$SYS/#", 0)

	# mqttc.username_pw_set('bmzrmflw', 'h7hmUII91mvS')
	mqttc.username_pw_set('iajmzgae', 'bNl5xzae8mox')
	mqttc.connect("m12.cloudmqtt.com", 16186, 60)
	mqttc.subscribe("SmartPlug", 0)
	mqttc.subscribe("SmartPlugData", 0)

	@sched.scheduled_job('interval', seconds = 50)
	def nudgeServer():
		res = curl(HOST_URL)

		print res
		return res	

	@sched.scheduled_job('interval', minutes = 1)
	def restartMQTTC():
		p = mp.Process(target = mqttc.loop_forever)
		p.start()
		p.join(timeout = 59)
		if p.is_alive():
			print "Terminating mqttc"
   			p.terminate()

   	sched.start()

@app.route('/')
def wakeServer():
	return "<span>MQTT up and running!</span>"

def startServer():
	time.sleep(10)	# Wait for flask app initialization
	res = curl(HOST_URL)
	print "Initial MQTT wakeup."

if __name__ == '__main__':
	# TODO: start server without request on browser
	# p = mp.Process(target = startServer)
	# p.start()
	app.logger.addHandler(logging.StreamHandler(sys.stdout))
	app.logger.setLevel(logging.ERROR)
	app.run(debug=True, use_reloader=False)


