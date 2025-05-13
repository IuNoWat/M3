#!/usr/bin/python
#coding: utf-8

import serial
import time
from threading import Thread

class Arduino(Thread) :
    def __init__(self) :
        Thread.__init__(self)
        self.api=serial.Serial("/dev/ttyACM0",9600,timeout=1)
        self.on=True
        self.unicode_error=0
        self.msg="coucou"
    def run(self) :
        while self.on :
            try :
                self.msg=self.api.read_until().decode()
            except UnicodeDecodeError :
                self.unicode_error+=1
    def get_msg(self) :
        to_return=self.msg[:7]
        if len(to_return)<6 :
            print("LE MESSAGE DE L'ARDUINO N'EST PAS ASSEZ LONG : ")
            print(self.msg)
            return "666666"
        return to_return


if __name__=="__main__" :
    while True :
        rah=Arduino()
        rah.start()
        for i in range(0,10) :
            time.sleep(1)
            print(rah.get_msg())
        rah.join()
