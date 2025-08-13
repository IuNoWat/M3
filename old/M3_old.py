#!/usr/bin/python
#coding: utf-8

import time
import random
import sys
import os

import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)

import arduino_serial as arduino
os.system("sudo pigpiod") #pigpoid needs to be launched before importing the buzzer library
import buzzer

#CONSTANTS
FPS=30
SCREEN_SIZE=(1920, 1080)
FULLSCREEN=True
RESET_ANIMATION_TIME=40

try :
    if sys.argv[1]=="debug" :
        DEBUG=True
except IndexError :
    DEBUG=False

#DATA

#M3 - Salon
#Lampe : 4 kWh
#Imprimante : 12 kWh
#Box Internet : 97 kWh
#Console : 103 kWh
#PC Fixe : 123 kWh
#Télévision : 162 kWh

#M3 - Cuisine
#Micro-Onde : 39 kWh
#Bouilloire : 49 kWh
#Plaques de cuisson : 131 kWh
#Lave-vaisselle : 162 kWh
#Seche-linge : 301 kWh
#Refrigerateur : 346 kWh

#STYLE OF THE APP

#ASSETS
NUM_FONT_PATH="/home/vaisseau/Desktop/M3/assets/DS-DIGI.TTF"
TXT_FONT_PATH="/home/vaisseau/Desktop/M3/assets/Rubik-VariableFont_wght.ttf"

#COLORS
WHITE=pygame.Color("White")
BLACK=pygame.Color("Black")
GREEN=pygame.Color("Green")
RED=pygame.Color("Red")
COLOR_BG=pygame.Color(22,13,34,255)
COLOR_HL=pygame.Color(255,255,255,255)

FONT_SIZE=30
FONT_STYLE=NUM_FONT_PATH
FONT_COLOR=COLOR_HL

debug_font=pygame.font.Font(TXT_FONT_PATH,16)

#GAMEPLAY
texts=[
    "39 kWh",
    "49 kWh",
    "131 kWh",
    "162 kWh",
    "301 kWh",
    "346 kWh"
]

#POSITION OF NUMBERS
number_pos=[
    (100, 100 ),
    (350, 100 ),
    (600, 100 ),
    (850, 100 ),
    (1100,100),
    (1350,100),
]

#NUMBER CLASS
class Number() :
    def __init__(self,pos,analogEntry,txt_number) :
        self.pos=pos
        self.current_pos=pos
        self.analogEntry=analogEntry
        self.value=False
        self.txt_number=txt_number
        self.int_number=int(txt_number)
        self.status="unconnected"
        self.woobling_timer=0
        self.animation_playing=False
        #Style des nombres
        self.font_size=20
        self.font = pygame.font.Font(NUM_FONT_PATH,FONT_SIZE)
    def update(self,last_values) :
        self.value=last_values[self.analogEntry]
        if self.value=="6" :
            self.status="unconnected"
        elif self.value==self.int_number :
            self.status=True
        else :
            self.status=False
        
        if self.woobling_timer>0 :
            self.woobling_timer-=1
        if self.woobling_timer==0 :
            self.animation_playing=False

    def start_reset_anim(self) :
        if self.animation_playing==False : 
            self.woobling_timer=RESET_ANIMATION_TIME
            self.animation_playing=True

    def render(self) :
        if DEBUG :
            txt=f"{self.value} - "+texts[self.txt_number]+f" ({self.txt_number})"
        else :
            txt=texts[self.txt_number]

        if self.status=="unconnected" :
            to_return=self.font.render(txt,1,COLOR_HL,COLOR_BG)
        elif self.status :
            to_return=self.font.render(txt,1,GREEN,COLOR_BG)
        else :
            to_return=self.font.render(txt,1,RED,COLOR_BG)

        if self.animation_playing :
            self.current_pos=(self.pos[0]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer),self.pos[1]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer))
        else :
            self.current_pos=self.pos
        return to_return

#MAINLOOP PREPARATION
running=True
SCREEN = pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN)
CLOCK = pygame.time.Clock()
good_cables=0
reset_timer=0
victory_timer=0


NUMBERS=[]
for i,pos in enumerate(number_pos) :
    NUMBERS.append(Number(pos,i,i))

#Launching thread
thread=arduino.Arduino()
thread.start()

#MAINLOOP
while running :
    #Cleaning of Screen
    SCREEN.fill(COLOR_BG)

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            thread.join()

    #Value update
    arduino_values=thread.get_msg()
    
    #Reset handling
    if reset_timer>0 :
        reset_timer-=1
        if reset_timer==0 :
            to_give=[0,1,2,3,4,5]
            for i,number in enumerate(NUMBERS) :
                new_number=random.choice(to_give)
                if i!=0 :
                    while new_number==number.txt_number :
                        new_number=random.choice(to_give)
                else :
                    new_number=NUMBERS[5].txt_number
                number.txt_number=new_number
                to_give.remove(new_number)

    #Numbers rendering
    for number in NUMBERS :
        number.update(arduino_values)
        SCREEN.blit(number.render(),number.current_pos)

    #Check of good cables
    good_cables=0
    for number in NUMBERS :
        if number.status==True :
            good_cables+=1
    
    #Victory check
    if good_cables==6 and reset_timer==0 and victory_timer==0 :
        victory_sound=buzzer.Sound(buzzer.default_music)
        victory_sound.start()
        victory_timer=90
    
    #Victory timer handling
    if victory_timer>0 :
        victory_timer-=1
        if victory_timer==0 :
            for number in NUMBERS :
                victory_sound.join()
                number.start_reset_anim()
                reset_timer=RESET_ANIMATION_TIME
                
    #Show FPS
    if DEBUG :
        fps = str(round(CLOCK.get_fps(),1))
        txt = "DEBUG MODE | FPS : "+fps+f" | Reset_timer : {reset_timer} | Data from arduino : {arduino_values} | Error passed in arduino thread : "+str(thread.unicode_error)
        to_blit=debug_font.render(txt,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,(0,0))

    #End of loop
    pygame.display.flip()
    CLOCK.tick(FPS)

