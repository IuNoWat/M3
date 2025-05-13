#!/usr/bin/python
#coding: utf-8

import time
import random

import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()

import arduino_serial as arduino

#CONSTANTS
FPS=30
SCREEN_SIZE=(1600, 900)
FULLSCREEN=True
DEBUG=True

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

#STYLE OF NUMBER
FONT_SIZE=30
FONT_STYLE=NUM_FONT_PATH
FONT_COLOR=COLOR_HL
RESET_ANIMATION_TIME=40

debug_font=pygame.font.Font(TXT_FONT_PATH,16)

#GAMEPLAY
texts=[
    "0 kWh",
    "4 kWh",
    "25 kWh",
    "357 kWh",
    "700 kWh",
    "2 000 kWh"
]

#POSITION OF NUMBERS
number_pos=[
    (100,450 ),
    (350,450 ),
    (600,450 ),
    (850,450 ),
    (1100,450),
    (1350,450),
]

#NUMBER CLASS
class Number() :
    def __init__(self,pos,analogEntry,txt_number) :
        self.pos=pos
        self.current_pos=pos
        self.analogEntry=analogEntry
        self.value=False
        self.txt_number=txt_number
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
        elif self.value==str(self.txt_number) :
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
        txt=f"{self.value} - "+texts[self.txt_number]+f" ({self.txt_number})"

        if self.status=="unconnected" :
            to_return=self.font.render(txt,1,COLOR_HL,COLOR_BG)
        elif self.status :
            to_return=self.font.render(txt,1,GREEN,COLOR_BG)
        else :
            to_return=self.font.render(txt,1,RED,COLOR_BG)

        if self.animation_playing :
            self.current_pos=(self.pos[0]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer),self.pos[1]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer))
            #elf.current_pos[0]=self.pos[0]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer)
            #elf.current_pos[1]=self.pos[1]+random.randrange(-RESET_ANIMATION_TIME+self.woobling_timer,RESET_ANIMATION_TIME-self.woobling_timer)
        else :
            self.current_pos=self.pos
        return to_return

#MAINLOOP PREPARATION
running=True
SCREEN = pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN)
CLOCK = pygame.time.Clock()
NUMBERS=[]
good_cables=0
reset_timer=0
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
        #if pygame.mouse.get_pressed() :
        #    running = False

    #Value update
    arduino_values=thread.get_msg()
    
    #Numbers rendering
    for number in NUMBERS :
        number.update(arduino_values)
        SCREEN.blit(number.render(),number.current_pos)
    
    #Victory check
    good_cables=0
    for number in NUMBERS :
        if number.status==True :
            good_cables+=1
    
    if good_cables==6 :
        for number in NUMBERS :
            number.start_reset_anim()
            reset_timer=RESET_ANIMATION_TIME-4
    
    if reset_timer>0 :
        reset_timer-=1
        if reset_timer==0 :
            to_give=[0,1,2,3,4,5]
            for i,number in enumerate(NUMBERS) :
                new_number=random.choice(to_give)
                while new_number==number.txt_number :
                    new_number=random.choice(to_give)
                number.txt_number=new_number
                to_give.remove(new_number)
                
    #Show FPS
    if DEBUG :
        fps = str(round(CLOCK.get_fps(),1))
        txt = "DEBUG MODE | FPS : "+fps+f" | Data from arduino : {arduino_values} | Error passed in arduino thread : "+str(thread.unicode_error)
        to_blit=debug_font.render(txt,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,(0,0))

    #End of loop
    pygame.display.flip()
    CLOCK.tick(FPS)

