# echo-client.py

import socket
import network
from time import sleep
from picozero import pico_led
from machine import Pin, Timer
# import uasyncio
import _thread


#HOST = "heartbutton.blueberrypi.studio"  # The server's hostname or IP address
HOST = "192.168.1.251"
PORT = 2000  # The port used by the server

ssid = 'Boul Family Wifi'

loveLED = Pin(0, Pin.OUT)
warnLED = Pin(2, Pin.OUT)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

def get_password():
    """Hide password from main file"""
    with open("password.txt") as file:
        return file.readline().rstrip() # returns password string

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, get_password())
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print("connected")

def listen(s):
    while True:
            print(f"Recieved: {s.recv(1024)}")


connect() # connect to internet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = socket.getaddrinfo(HOST, PORT, 0, socket.SOCK_STREAM)[0][-1] 
print(server) 

s.connect(server)
packet = bytearray(2)
packet[0] = 1
packet[1] = 8

_thread.start_new_thread(listen, [s])


try:
    while True:
        if button.value():
            print(f"sent packet: {packet}")
            s.sendto(packet, server)
            loveLED.toggle()

            sleep(1)
except KeyboardInterrupt:
#     s.close()
    print("Stopping")


s.close()