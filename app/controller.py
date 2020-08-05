from config import Config
from logger import setup_logger
from updater import Updater
import logging, datetime, time, atexit, json, multiprocessing

id = "GPIO controller: "

# GPIO init
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print(id + "Error importing RPi.GPIO, switching to mock up")
    import test_io as GPIO

# Initial setup
def init_enviroment_config():

    with open(Config.state_file) as json_file:
        data = json.load(json_file)
        if data != None:
            environment_config = data

        else:
            environment_config = {
                "temp" : "0.0",
                "tempUnits" : "C",
                "humidity" : "0.0",
                "elapsed" : "0",
                "mode" : "off",
                "fan_state" : "on",
                "light_state" : "on",
                "pump_state" : "off"
            }

# Updated config flag
environment_config = init_enviroment_config()

# Job functions
def water(action, forLength=None):
	toggleComponent(Config.PUMP_PIN, action, forLength)

def fan(action, forLength=None):
    toggleComponent(Config.FAN_PIN, action, forLength)

def light(action, forLength=None):
	toggleComponent(Config.LIGHT_PIN, action, forLength)

def toggleComponent(pin, action, forLength=None):
	if (forLength is not None):
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(forLength)
		GPIO.output(pin, GPIO.LOW)
	else:
		if action == Config.START_ACTION: GPIO.output(pin, GPIO.HIGH)
		else: GPIO.output(pin, GPIO.LOW)

# Update function that catches incoming config changes from the web server
def check_for_updates():
    while True:
        updater = Updater(Config.web_controller_conn_str)
        message = updater.run()
        time.sleep (1) 
        if message != None:
            environment_config = message
            with open(Config.state_file, 'w') as outfile:
                json.dump(environment_config, outfile)
        print('update done')

# Enviroment control function
def eval_environment_state():
    while True:
        print('eval done')
        time.sleep(5)

def exit_handler():
    GPIO.cleanup()

atexit.register(exit_handler)

# Main
def main():
    #log
    time.sleep(1)

if __name__ == '__main__':

    # Logger setup
    logger = setup_logger("master", Config.master_log_file, logging.DEBUG)

    # Pin setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Config.LIGHT_PIN, GPIO.OUT)
    GPIO.setup(Config.PUMP_PIN, GPIO.OUT)

    update_process = multiprocessing.Process(target=check_for_updates)
    environment_process = multiprocessing.Process(target=eval_environment_state)

    print(id + "Starting Fatman environmnet config updater...")
    update_process.start()
    print(id + "Starting Fatman environmnet control process...")
    environment_process.start()
    print(id + "Starting main process...")

    while True:
        main()