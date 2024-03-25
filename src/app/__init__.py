import machine
from machine import Pin
import sys
import utime

def run():
    with open('data/example.txt') as f:
        data = f.read()
        
    print("example data: {}".format(data))
    
    board = sys.implementation._machine.split(' with')[0]
    print(f"Running on {board} ({sys.platform}) at {machine.freq() / 1000000} MHz")

    led = Pin(25, Pin.OUT) # onboard LED
    counter = 0
    while True:
        counter += 1
        print(f"Uptime: {counter} seconds")
        led.toggle()
        utime.sleep_ms(1000)

if __name__ == "__main__":
    print("running app.py file directly")
    run()