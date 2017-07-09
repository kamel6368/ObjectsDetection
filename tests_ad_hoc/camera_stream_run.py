import cv2
from Common.TCPConnections import TCPClient
from Common.config import config
import Common.image_serialization as im_ser
import time
from Common.Logger import Logger

address = "127.0.0.1"
port = 2465

logger = Logger()

client = TCPClient(address, port, logger)
client.connect()

camera = cv2.VideoCapture(0)
for i in range(10):
    camera.read()

while True:
    print 'in'
    _, img = camera.read()

    img_str = im_ser.image_to_string(img)

    org_image = im_ser.image_from_string(img_str)

    #cv2.imshow('dadsdas', org_image)
    #cv2.waitKey(1)

    client.send('IMAGE', img_str)
