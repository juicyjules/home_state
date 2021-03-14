import requests
from time import sleep
import json
import colour
import pigpio
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from websocket import create_connection

API_KEY = "bf2c4222-f33e-408d-bb87-8db25e13db39"
MASTER_KEY = "4ac25e64-6985-46dd-9878-0bae91c48519"
URL = f"http://localhost:8000/client/{API_KEY}/info"
REALTIME_URL = f'ws://localhost:8000/ws/realtime/{MASTER_KEY}/'
POLLING_TIME = 200
LED = {
    "R" : 17,
    "G" : 27,
    "B" : 24,
}
session = requests.Session()
retry = Retry(connect=10000, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://",adapter)
def getData():
    response = session.get(URL,timeout=2)
    data = response.json()
    return data
def setLED(pi,led,brightness):
    pi.set_PWM_dutycycle(led,brightness)
    return
def setColor(pi,color):
    for pin,brightness in zip(LED.values(),color):
        setLED(pi,pin,255*brightness)

def realtime_loop(socket,pi):
    while True:
        data = socket.recv()
        data = json.loads(data)
        if not data["realtime"]:
            return
        setColor(pi, colour.hex2rgb(data["color"]))
def main():
    #pi = pigpio.pi()
    realtime = False
    pi = None
    print("Starting up...")
    while True:
        penalty = 0
        try:
            if not realtime:
                data = getData()
                #print(data)
                if (data["realtime"]):
                    realtime = True
                    continue
                if (data["on"]):
                    color = colour.hex2rgb('#'+data["color"])
                    setColor(pi,color)
                else:
                    penalty = 1000
                    setColor(pi,colour.hex2rgb("#000000"))
                sleep((penalty + POLLING_TIME) / 1000)
            else:
                socket = create_connection(REALTIME_URL)
                realtime_loop(socket,pi)
                realtime = False
        except Exception as e:
            pi.stop()
            pi = pigpio.pi()
            print(e)
            sleep(5000)
main()
