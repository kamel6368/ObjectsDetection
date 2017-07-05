from time import sleep
from Common.config import config

from Common.TCPConnections import TCPClient

data = 'ala ma kota'
address = config('Agent/ip')
port = config('Agent/port')

client = TCPClient(address, port)

client.connect()
while True:
    client.send(data)
    sleep(2)