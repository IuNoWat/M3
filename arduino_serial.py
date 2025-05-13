
import serial

arduino=serial.Serial("/dev/ttyACM0",9600,timeout=1)


if __name__=="__main__" :
    while True :
        print(arduino.readline())