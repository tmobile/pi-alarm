# coding=utf-8
# =========================================================================
# Copyright © 2018 T-Mobile USA, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================
#
# Raspberry Pi Alarm
# 
# https://github.com/tmobile/pi-alarm
#

from flask import request
from flask_api import FlaskAPI
from flask_cors import CORS
from threading import Timer
import os
import datetime
import sys
import argparse
import yaml
import logging
import logging.config
import logging.handlers
import subprocess
import webbrowser

VERSION = "1.0.0"

PORT = 80
DEFAULT_PIN = 18
TIMEOUT = 60
ENABLE_PI = True
ENABLE_SOUND = False
ENABLE_DEBUGGER = False
ENABLE_LAUNCH_BROWSER = True
PLATFORM_LIST = ("darwin","win32","cygwin")

LOGGING_CONF = os.path.dirname(os.path.realpath(__file__)) + "/logging.conf.yaml"
LOG_FILE = os.path.dirname(os.path.realpath(__file__)) + "/alarm.log"
KEY_FILE = os.path.dirname(os.path.realpath(__file__)) + "/key_file.txt"

if os.path.isfile(LOGGING_CONF):
	flask_log = logging.getLogger('werkzeug') 		# Set Flask logging level to error
	flask_log.setLevel(logging.ERROR)
	with open (LOGGING_CONF, 'rt') as f:
	   config=yaml.safe_load(f)
	   config['handlers']['rotating_file_handler']['filename']=LOG_FILE
	logging.config.dictConfig(config)

app = FlaskAPI(__name__)
CORS(app)

if sys.platform in PLATFORM_LIST:
	ENABLE_PI = False
	PORT = 1080

if ENABLE_PI:
	import RPi.GPIO as GPIO #pylint: disable=import-error
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)

def process_arguments(args):
	global ENABLE_DEBUGGER, PORT, TIMEOUT
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", help="Enable debug mode (default disabled)", action="store_true")
	parser.add_argument("-p", "--port", help="Listen port (default 80)")
	parser.add_argument("-t", "--timeout", help="Alarm on timeout in seconds (default 60)")
	parser.add_argument("-v", "--version", help="Display version number", action="version", version=VERSION)

	args = parser.parse_args(args)

	if args.debug:
		ENABLE_DEBUGGER = args.debug

	if args.port:
		PORT = int(args.port)

	if args.timeout:
		TIMEOUT = int(args.timeout)

process_arguments(sys.argv[1:])

user_access_log = {}
switch_state = {}
timer_threads = {}

def turn_on(pin, timeout):
	global switch_state
	switch_state[pin] = "on"
	if ENABLE_PI:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,GPIO.HIGH)
	new_timer = Timer(int(timeout), turn_off, [pin])
	new_timer.start()
	if pin in timer_threads:
		timer = timer_threads[pin]
		if timer:
			timer.cancel()
			del timer_threads[pin]
	timer_threads[pin] = new_timer
	logging.info("Turn on pin " + str(pin) + " 🚨")

def turn_off(pin):
	global switch_state
	switch_state[pin] = "off"
	if ENABLE_PI:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,GPIO.LOW)
	if pin in timer_threads:
		timer = timer_threads[pin]
		if timer:
			timer.cancel()
			del timer_threads[pin]
	logging.info("Turn off pin " + str(pin)+ " 🔕")

def play_sound():
	if ENABLE_PI and ENABLE_SOUND:
		os.system('mpg123 -q siren1.mp3 &')

def load_keys():
	global key_file, keys
	keys = {}
	if os.path.isfile(KEY_FILE):
		key_file = open(KEY_FILE, "r")
		content = key_file.readlines()
		key_count = 0
		for line in content:
			line = line.strip()
			if not(line.startswith("#")):
				key_count += 1
				user,access_key,pin,url = line.split(",")
				user = user.strip()
				access_key = access_key.strip()
				pin = pin.strip()
				url = url.strip()
				if pin == False or pin == "":
					pin = DEFAULT_PIN
				keys[access_key] = {
					'user':user,
					'pin':pin,
					'url':url}

def reset_timers():
	for pin, timer in timer_threads.items():
		if timer:
			timer.cancel()
		del timer_threads[pin]

def cleanup():
	try:
		key_file.close()
		reset_timers()
	except Exception:
		return

def keys_exist():
	if len(keys) == 0:
		return False
	else:
		return True

def check_key(key):
	if key in keys:
		return keys[key]
	else:
		return False

def open_url(url):
	if ENABLE_LAUNCH_BROWSER and url:
		webbrowser.open_new_tab(url)
		logging.info("Open browser " + url)

def mask_sensitive_data(data):
	if data and 'access_key' in data.keys():
		data['access_key'] = "***"
	return data

def log_user(user, state, request):

	json_data = mask_sensitive_data(request.get_json(silent=True))
	logging.info("%s|%s|%s|%s", user, request.remote_addr, request.url, json_data )

	if user not in user_access_log:
		user_access_log[user] = {}
		user_access_log[user]['count'] = 1
	else:
		user_access_log[user]['count'] += 1
	user_access_log[user]['last_access'] = datetime.datetime.now()

def get_ip_address():
	ip = ""
	try:
		ip = subprocess.check_output(["hostname","-I"]) 
		ip = ip.decode("utf-8").strip() 
	except Exception:
		logging.info("Could not get IP address")
	return ip

def banner_info():
	logging.info("Pi Alarm " + VERSION)
	logging.info("Platform: " + sys.platform)
	if ENABLE_PI:
		logging.info("IP: " + get_ip_address())
	logging.info("Port: " + str(PORT))
	logging.info("Timeout: " + str(TIMEOUT))
	logging.info("Enable Pi: " + str(ENABLE_PI))
	logging.info("Keys: " + str(len(keys)))
	logging.info("Debug mode: " + str(ENABLE_DEBUGGER))

@app.route('/', methods=["GET"])
def home():
	return {
		"message" : "Welcome to the Raspberry Pi Alarm!"
	}

@app.route('/alarm/<state>', methods=["GET", "POST"])
def alarm_control(state):
	timeout = TIMEOUT
	user = "guest"
	pin = DEFAULT_PIN
	url = False

	try:
		content = request.get_json(silent=False)
		if keys_exist():
			authorized = False
			access_key = ""
			if not(content is None) and ('access_key' in content):
				access_key = content['access_key']
				data = check_key(access_key)
				if not data == False:
					user = data['user']
					pin = data['pin']
					url = data['url']
					authorized = True
			if not authorized:
				logging.info("Unauthorized access|%s|%s", request.remote_addr, access_key)
				return {
				    "status" : "error",
					"message": "unauthorized" }, 403
		if not(content is None):
			if 'timeout' in content:
				timeout = content['timeout']
			if 'url' in content:
				url = content['url']
 
		log_user(user, state, request)

		if (state == "on"):
			turn_on(pin, timeout)
			play_sound()
			open_url(url)
		elif (state == "off"):
			turn_off(pin)

		return {
			"status" : "OK",
			"alarm" : switch_state[pin],
			"timeout" : timeout,
			"pin" : pin
		}
	except Exception as e:
		log_user("Error", str(e), request)
		logging.exception(e)
		return {
			"status" : "error",
			"message" : str(e)
		}, 400

@app.route('/info', methods=["GET"])
def info():
	return {
		"status" : "OK",
		"version" : VERSION,
		"platform" : sys.platform,
		"pi enabled" : ENABLE_PI,
		"alarm" : switch_state,
		"default timeout" : TIMEOUT,
		"keys" : len(keys),
		"users" : user_access_log
	}

@app.route('/logs', methods=["GET"])
def logs():
	content = ""
	if os.path.isfile(LOG_FILE):
		log_file = open(LOG_FILE, "r")
		content = log_file.readlines()
		log_file.close()
	return {
		"status" : "OK",
		"logs" : content
	}

@app.route('/ping', methods=["GET"])
def ping():
	return {
		"status" : "OK"
	}

@app.route('/reset', methods=["GET"])
def reset():
	global user_access_log

	user_access_log = {}
	load_keys()
	reset_timers()
	logging.info("Resetting")
	return {
		"status" : "OK"
	}

load_keys()

if __name__ == "__main__":
	banner_info()
	app.run(host='0.0.0.0', port=PORT, debug=ENABLE_DEBUGGER)
