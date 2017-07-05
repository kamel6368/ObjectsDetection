import cv2
from Common.TCPConnections import TCPClient
from Common.config import config
import base64
from time import sleep

data = 'ala ma kota'
address = config('Agent/ip')
port = config('Agent/port')

client = TCPClient(address, port)
client.connect()

camera = cv2.VideoCapture()

while True:
    _, img = camera.read()
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    client.send(jpg_as_text)
    sleep(1)
2