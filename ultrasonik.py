import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

echo = 24
trig = 23
trig_time = 0.00001

GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)

def get_distance():
	GPIO.output(trig, 0)
	time.sleep(0.000002)	
	GPIO.output(trig, 1)
	time.sleep(trig_time)
	GPIO.output(trig, 0)
	
	while GPIO.input(echo) == 0:
		startCount = time.time()
	
	while GPIO.input(echo) == 1:
		endCount = time.time()
	
	duration = endCount - startCount
	distance = (duration * 34300) / 2
	
	return distance
	
if __name__ == '__main__':
	try:
		while True:
			dist = get_distance()
			print("Measured Distance = %.1f cm" % dist)
			time.sleep(1)
	
	except KeyboardInterrupt:
		print("Measurement stopped")
		GPIO.cleanup()