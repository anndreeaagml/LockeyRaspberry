import requests
import RPi.GPIO as GPIO
import time
import re, uuid 
data = {
    "ID": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
    "IsLocked": True
}

r=requests.post('https://lockeyapi.azurewebsites.net/Sensor', data=data)
print(r)

a=requests.get('https://lockeyapi.azurewebsites.net/Sensor')
print(a._content.decode("utf-8"))
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

#initialise a previous input variable to 0 (Assume no pressure applied)
prev_input = 0
try:
    while True:
        #take a reading
        input = GPIO.input(4)
        #if the last reading was low and this one high, alert us
        if (prev_input > input):
            new_data={"IsLocked":False}
            data.update(new_data)
            r=requests.post('https://lockeyapi.azurewebsites.net/Sensor', data=data)
            print(r)
            print("Unlocked")
        #update previous input
        prev_input = input
        #slight pause
        time.sleep(0.10)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()