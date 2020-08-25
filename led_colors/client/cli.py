import requests
from time import sleep
import colour
#import pigpio
API_KEY = "bf2c4222-f33e-408d-bb87-8db25e13db39"
URL = f"http://localhost:8000/leds/client/{API_KEY}/info"
POLLING_TIME = 200
LED = {
    "R" : 17,
    "G" : 22,
    "B" : 24,
}
def getData():
    response = requests.get(URL)
    data = response.json()
    return data
def setLED(pi,led,brightness):
    pi.set_PWM_dutycycle(led,brightness)
def setColor(pi,color):
    for pin,brightness in zip(LED.values(),color):
        setLED(pi,pin,brightness)
def main():
    #pi = pigpio.pi()
    pi = None
    while True:
        data = getData()
        color = colour.hex2rgb('#'+data["color"])
        setColor(pi,color)
        sleep(POLLING_TIME / 1000)
main()