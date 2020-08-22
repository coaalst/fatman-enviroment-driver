from modules.config import Config
from logger import setup_logger
from modules.updater import Updater
from modules.gpio_interface import Dispatcher
#from modules.temperature import Thermostat
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
            return data

        else:
            data = {
                "temp" : "0.0",
                "tempUnits" : "C",
                "humidity" : "0.0",
                "elapsed" : "0",
                "mode" : "auto",
                "fan_state" : "on",
                "light_state" : "on",
                "pump_state" : "off",
                "interval_start" : 23,
                "interval_stop" : 11
            }
            return data

            # Serializing json  
            with open(Config.state_file, 'w') as outfile:
                json.dumps(environment_config, outfile)

# Update function that catches incoming config changes from the web server
def check_for_updates():
    while True:
        updater = Updater(Config.web_controller_conn_str)
        message = updater.run()
        time.sleep (1) 
        if message != None:
            Config.environment_config = message
            with open(Config.state_file, 'w') as outfile:
                json.dumps(message, outfile)
        print('update done')

# Light scheduel check function
def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

# Enviroment control function
def eval_environment_state():
    while True:
        #temperature = Thermostat.read_temp()
        temperature = 26
        light_flag = time_in_range(datetime.time(Config.environment_config.interval_start, 0, 0), datetime.time(Config.environment_config.interval_stop, 0, 0), datetime.now())
        if Config.environment_config.mode == "auto":
            if temperature >= Config.environment_config.temp:
                Dispatcher.fan(1, None)
            else:
                Dispatcher.fan(0, None)

            if light_flag == True:
                Dispatcher.light(1, None)
            else:
                Dispatcher.light(0, None)

        else:
            if Config.environment_config.fan_state == "on":
                Dispatcher.fan(1, None)
            else:
                Dispatcher.fan(0, None) 

            if Config.environment_config.pump_state == "on":
                Dispatcher.pump(1, None)
            else:
                Dispatcher.pump(0, None)
            
            if Config.environment_config.light_state == "on":
                Dispatcher.light(1, None)
            else:
                Dispatcher.light(0, None)

        print('eval done')

        time.sleep(5)

def exit_handler():
    GPIO.cleanup()

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

    atexit.register(exit_handler)

    # Updated config flag
    Config.environment_config = init_enviroment_config()

    update_process = multiprocessing.Process(target=check_for_updates)
    environment_process = multiprocessing.Process(target=eval_environment_state)

    print(id + "Starting Fatman environmnet config updater...")
    update_process.start()
    print(id + "Starting Fatman environmnet control process...")
    environment_process.start()
    print(id + "Starting main process...")

    while True:
        main()
