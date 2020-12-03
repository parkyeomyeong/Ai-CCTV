""" import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
buzzer=23 
GPIO.setup(buzzer,GPIO.OUT)
 """

def buzzer_control(input):
    if(input == "ON"):
        print("haha")
    elif(input == "OFF"):
        print("hoho")

""" while True:
    GPIO.output(buzzer,GPIO.HIGH)
    sleep(0.5) # Delay in seconds
    GPIO.output(buzzer,GPIO.LOW)
    sleep(0.5) """