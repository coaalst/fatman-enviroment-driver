id = "GPIO controller: "

# GPIO init
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    print(id + "Error importing RPi.GPIO, switching to mock up")
    pass
import time

# Mock up for testing io
class GPIO:
	BCM = 1
	OUT = 1
	IN = 1
	RISING = 1
	HIGH = 1
	LOW = 0

	def output(pin, value):
	    pass

	def setmode(mode):
	    pass

	def setup(pin, mode):
	    pass

	def add_event_detect(pin, edge, callback, bouncetime):
	    pass

	def cleanup():
	    pass


LIGHT_PIN = 20
PUMP_PIN = 12
FAN_PIN = 13

START_ACTION = 1
STOP_ACTION = 0

 # Pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(PUMP_PIN, GPIO.OUT)

class Dispatcher():

	def pump(action, forLength = None):
		toggleComponent(PUMP_PIN, action, forLength)

	def fan(action, forLength=None):
		toggleComponent(FAN_PIN, action, forLength)

	def light(action, forLength=None):
		toggleComponent(LIGHT_PIN, action, forLength)

def toggleComponent(pin, action, forLength):
	if forLength is not None:
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(forLength)
		GPIO.output(pin, GPIO.LOW)
	else:
		if action == START_ACTION:
			GPIO.output(pin, GPIO.HIGH)
			print(id + str(pin) + " is on")
		else:
			GPIO.output(pin, GPIO.LOW)
			print(id + str(pin) + " is off")

