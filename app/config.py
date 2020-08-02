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
    state_file = "state.json"

    # Switch data
    switches = ['1']
    on_pins = [9, 1, 7]
    off_pins = [11, 0, 8]
    switch_pulse_time_in_secs = 1.5

    # ZMQ Connection stuff
    web_controller_conn_str = "tcp://127.0.0.1:2000"
    
    # Logging files
    web_log_file = "fatman_web.log"
    master_log_file = "fatman_master.log"
    gpio_log_file = "fatman_gpio.log"

