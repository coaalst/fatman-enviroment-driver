import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    NAME = "enviroment_control_service"
    LIGHT_PIN = 20
    PUMP_PIN = 12
    FAN_PIN = 13
    START_ACTION = "on"
    STOP_ACTION = "off"

    # Web interface settings
    hostname = "0.0.0.0"

    port = 8007
    state_file = basedir + "/environment_config.json"

    # ZMQ Connection stuff
    web_controller_conn_str = "tcp://127.0.0.1:2000"
    
    # Logging files
    web_log_file = "fatman_web.log"
    master_log_file = "fatman_master.log"
    gpio_log_file = "fatman_gpio.log"

