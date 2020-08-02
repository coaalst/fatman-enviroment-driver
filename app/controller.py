from config import Config
from logger import setup_logger

import threading
import zmq
import logging
import datetime
import time
import atexit
import json

# Logger setup
id = "GPIO controller: "
logger = setup_logger("master", settings.master_log_file, logging.DEBUG)

# GPIO init
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print(id + "Error importing RPi.GPIO, switching to mock up")
    import test_io as GPIO


# Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)


# ZMQ setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.bind(Config.web_controller_conn_str)

# Job functions
def water(action, forLength=None):
	threaded(toggleComponent(Config.PUMP_PIN, action, forLength))

def fan(action, forLength=None):
    threaded(toggleComponent(Config.FAN_PIN, action, forLength))

def light(action, forLength=None):
	threaded(toggleComponent(Config.LIGHT_PIN, action, forLength))

# Threaded adapter for jobs
def threaded(job_func, action=Config.START_ACTION, forLength=None):
    job_thread = threading.Thread(target=job_func, kwargs={'action': action, 'forLength': forLength})
    job_thread.start()

def toggleComponent(pin, action, forLength=None):
	if (forLength is not None):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(forLength)
		GPIO.output(pin, GPIO.LOW)
	else:
		if action == Config.START_ACTION: GPIO.output(pin, GPIO.HIGH)
		else: GPIO.output(pin, GPIO.LOW)

# Main function that checks the enviroment status and issues commands
def main():
    # Get temp - handle change
    # Get humidity - handle change
    # Check ZMQ for requests
    message = socket.recv()
    if message != None:
        environment_config = message
        with open('environment_config.json', 'w') as outfile:
            json.dump(environment_config, outfile)

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)

while True:
    main()
    time.sleep(1)