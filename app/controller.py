import os
from logger import setup_logger
from modules.updater import Updater
from modules.gpio_interface import Dispatcher
#from modules.sensor_interface import Fetcher

import logging, datetime, time, json, multiprocessing
from configparser import ConfigParser

id = "Controller: "

# Initial setup
def init_enviroment_config(config):

   return config.read(os.path.abspath(os.path.dirname(__file__)) + "\..\conf_data.properties")

# Update function that catches incoming config changes from the web server
def check_for_updates():
    while True:
        updater = Updater("tcp://127.0.0.1:2000")
        message = updater.run()
        time.sleep (1) 
        if message != None:
            with open(os.path.abspath(os.path.dirname(__file__)) + "\..\conf_data.properties", 'w') as outfile:
                json.dumps(message, outfile)
        print('update done')

# Light scheduel check function
def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

# Fetches data from the arduino controller via Serial
def fetch_sensor_data():
    pass

# Enviroment control function
def eval_environment_state(conf_data):
    while True:
        #temperature, humidity = Fetcher.fetch_sensor_data()
        temperature = 26
        humidity = 50
        light_flag = time_in_range(datetime.time(int(conf_data["interval_start"]), 0, 0), datetime.time(int(conf_data["interval_stop"]), 0, 0), datetime.time())

        if conf_data["mode"] == "auto":
            if temperature >= float(conf_data["temp"]):
                Dispatcher.fan(1, None)
            else:
                Dispatcher.fan(0, None)

            if light_flag == True:
                Dispatcher.light(1, None)
            else:
                Dispatcher.light(0, None)

            if humidity <= float(conf_data["humidity"]):
                Dispatcher.pump(1, None)
            else:
                Dispatcher.pump(0, None)

        else:
            if conf_data["fan_state"] == "on":
                Dispatcher.fan(1, None)
            else:
                Dispatcher.fan(0, None) 

            if conf_data["pump_state"] == "on":
                Dispatcher.pump(1, None)
            else:
                Dispatcher.pump(0, None)
            
            if conf_data["light_state"] == "on":
                Dispatcher.light(1, None)
            else:
                Dispatcher.light(0, None)

        print('eval done')

        time.sleep(5)

# Main
def main():
    #log
    time.sleep(1)


if __name__ == '__main__':

    # Logger setup
    logger = setup_logger("master", "fatman_master.log", logging.DEBUG)

    # Parser
    config = ConfigParser()

    # Updated config flag
    conf_data = init_enviroment_config(config)

    conf_data = {
        "temp" : "0.0",
        "tempUnits" : "C",
        "humidity" : "60.0",
        "elapsed" : "0",
        "mode" : "auto",
        "fan_state" : "on",
        "light_state" : "on",
        "pump_state" : "off",
        "interval_start" : 23,
        "interval_stop" : 11
    }   
    print(conf_data)
    update_process = multiprocessing.Process(target=check_for_updates)
    environment_process = multiprocessing.Process(target=eval_environment_state, args=(conf_data, ))

    print(id + "Starting Fatman environmnet config updater...")
    update_process.start()
    print(id + "Starting Fatman environmnet control process...")
    environment_process.start()
    print(id + "Starting main process...")

    while True:
        main()
