import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=23 
GPIO.setup(buzzer,GPIO.OUT)


def buzzer_control(input):
    if(input == "ON"):
        GPIO.output(buzzer,GPIO.HIGH)
    elif(input == "OFF"):
        GPIO.output(buzzer,GPIO.LOW)
