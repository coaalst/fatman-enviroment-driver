START_ACTION = 1
STOP_ACTION = 0

class Dispatcher():

    # Job functions
    def pump(action, forLength=None):
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
    		if action == START_ACTION: GPIO.output(pin, GPIO.HIGH)
    		else: GPIO.output(pin, GPIO.LOW)
