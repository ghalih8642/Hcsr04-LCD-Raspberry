import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# deklarasi untuk sensor jarak ultrasonik
echo = 24
trig = 23
trig_time = 0.00001

GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)

# deklarasi untuk LCD
rs = 20
en = 21
d4 = 6
d5 = 13
d6 = 19
d7 = 26

GPIO.setup(rs, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)

def all_low():
	GPIO.output(rs, GPIO.LOW)
	GPIO.output(en, GPIO.LOW)
	GPIO.output(d4, GPIO.LOW)
	GPIO.output(d5, GPIO.LOW)
	GPIO.output(d6, GPIO.LOW)
	GPIO.output(d7, GPIO.LOW)

def lcd_port(a):
	GPIO.output(d4, GPIO.LOW)
	GPIO.output(d5, GPIO.LOW)
	GPIO.output(d6, GPIO.LOW)
	GPIO.output(d7, GPIO.LOW)
	if a & 0x01 == 0x01:
		GPIO.output(d4, GPIO.HIGH)

	if a & 0x02 == 0x02:
		GPIO.output(d5, GPIO.HIGH)

	if a & 0x04 == 0x04:
		GPIO.output(d6, GPIO.HIGH)

	if a & 0x08 == 0x08:
		GPIO.output(d7, GPIO.HIGH)

def lcd_cmd(b):
	GPIO.output(rs, GPIO.LOW)
	lcd_port(b)
	time.sleep(0.001)
	GPIO.output(en, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(en, GPIO.LOW)
	time.sleep(0.001)

def lcd_clear():
	lcd_cmd(0)
	lcd_cmd(1)

def lcd_setCursor(baris,kolom):
	x = 0
	y = 0
	
	if baris == 0:
		x = 0x08
		y = kolom
		lcd_cmd(x)
		lcd_cmd(y)
	
	else:
		x = 0x0C
		y = kolom
		lcd_cmd(x)
		lcd_cmd(y)

def lcd_init():
	lcd_cmd(0x02)

	lcd_cmd(0x02)
	lcd_cmd(0x08)

	lcd_cmd(0x00)
	lcd_cmd(0x0C)

	lcd_cmd(0x00)
	lcd_cmd(0x06)

def lcd_writeChar(datum):
	lsb = datum & 0x0F
	msb = datum & 0xF0
	GPIO.output(rs, GPIO.HIGH)
	lcd_port(msb>>4)
	time.sleep(0.001)
	GPIO.output(en, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(en, GPIO.LOW)
	time.sleep(0.001)
	lcd_port(lsb)
	time.sleep(0.001)
	GPIO.output(en, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(en, GPIO.LOW)
	time.sleep(0.001)

def lcd_writeString(data):
	i = 0
	for i in range(0, len(data)):
		lcd_writeChar(ord(data[i]))
		i = i + 1

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
		all_low()
		lcd_init()
		while True:
			dist = get_distance()
			lcd_clear()
			lcd_setCursor(0,0)
			lcd_writeString("jarak :")
			lcd_setCursor(1,0)
			disp = "%.1f"%dist + " cm"
			lcd_writeString(disp)
			time.sleep(1)
	
	except KeyboardInterrupt:
		print("Measurement stopped")
		GPIO.cleanup()