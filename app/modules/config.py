import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'fatman.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'fatcat'

    NAME = "enviroment_control_service"
    LIGHT_PIN = 20
    PUMP_PIN = 12
    FAN_PIN = 13
    HUMIDITY_SENSOR_PIN = 15
    TEMPERATURE_SENSOR_PIN = 16

    # Web interface settings
    hostname = "0.0.0.0"

    port = 8007
    state_file = basedir + "\..\environment_config.json"

    # ZMQ Connection stuff
    web_controller_conn_str = "tcp://127.0.0.1:2000"
    
    # Logging files
    web_log_file = "fatman_web.log"
    master_log_file = "fatman_master.log"
    gpio_log_file = "fatman_gpio.log"

    environment_config = {
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

