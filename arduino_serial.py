
import serial
import time

arduino=serial.Serial("/dev/ttyACM0",9600,timeout=1)

def get_arduino_info() :
    last_msg=arduino.readline()
    to_return=[
        last_msg[4:5],
        last_msg[12:13],
        last_msg[20:21],
        last_msg[28:29],
        last_msg[36:37],
        last_msg[44:45]
    ]
    arduino.flushInput()
    return to_return

if __name__=="__main__" :
    while True :
        print(f"Serial message : {arduino.readline()}")
        print(f"Traduction     : {get_arduino_info()}")
        time.sleep(0.1)
