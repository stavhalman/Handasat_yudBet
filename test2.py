import RPi.GPIO as GPIO


button1 = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN)

while True:
    if(GPIO.input(button1)):
        print("yay")
    else:
        print("no")