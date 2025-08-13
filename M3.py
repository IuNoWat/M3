import sys
import random
import time
import os

import pygame
pygame.init()

from tools import *
import arduino_serial as arduino
os.system("sudo pigpiod") #pigpoid needs to be launched before importing the buzzer library
import buzzer

#CONSTANTS
FPS=30
DIR="/home/vaisseau/Desktop/"
SCREEN_SIZE=(1920, 1080)
SCREEN = pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN)
FULLSCREEN=True
#Define DEBUG
try :
    if sys.argv[1]=="debug" :
        DEBUG=True
except IndexError :
    DEBUG=False
    pygame.mouse.set_visible(False)

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

#Animation CONSTANTS

#ASSETS LOAD
#FONTS
NUM_FONT_PATH=DIR+"M3/assets/DS-DIGI.TTF"
TXT_FONT_PATH=DIR+"M3/assets/Rubik-VariableFont_wght.ttf"
#IMG
plug_male_good=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_male_good.png").convert_alpha(),0.4)
plug_male_bad=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_male_bad.png").convert_alpha(),0.4)
plug_male_idle=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_male_idle.png").convert_alpha(),0.4)
plug_female_good=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_female_good.png").convert_alpha(),0.4)
plug_female_bad=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_female_bad.png").convert_alpha(),0.4)
plug_female_idle=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/plug_female_idle.png").convert_alpha(),0.4)
#elec=pygame.image.load(DIR+"M3/assets/elec.png").convert_alpha()

#STYLE
WHITE=pygame.Color("White")
BLACK=pygame.Color("Black")
GREEN=pygame.Color("Green")
RED=pygame.Color("Red")
COLOR_BG=pygame.Color(22,13,34,255)
COLOR_HL=pygame.Color(255,255,255,255)

NUM_FONT_SIZE=50
FONT_STYLE=NUM_FONT_PATH
FONT_COLOR=COLOR_HL

pygame.font.init()
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
    (320*0+320/2, 50 ),
    (320*1+320/2, 50 ),
    (320*2+320/2, 50 ),
    (320*3+320/2, 50 ),
    (320*4+320/2, 50),
    (320*5+320/2, 50),
]


#ENGINE

class Anim() : #Use this class as base for animations, see below with the Pop example
    def __init__(self,max_frame,loop=False) :
        self.max_frame=max_frame
        self.current_frame=0
        self.method=print
        self.finished=False
        self.loop=loop
    def anim(self) :
        self.method(self.current_frame)
        self.current_frame=self.current_frame+1
        if self.current_frame==self.max_frame :
            if self.loop :
                self.current_frame=0
            else :
                self.finished=True

class Pop(Anim) : # The Pop anim will play the moove method each frame until the max frame is reached
    def moove(self,current_frame) :
        self.img.set_alpha(255-current_frame*16)
        center_blit(SCREEN,self.img,(self.pos[0],self.pos[1]-current_frame*3))
    def __init__(self,max_frame,img,pos) :
        Anim.__init__(self,max_frame)
        self.img=img
        self.pos=pos
        self.method=self.moove
    def anim(self) :
        print(self.current_frame)
        Anim.anim(self)

#SPECIFIC ENGINE

class Number(Anim) :
    def render(self,current_frame) :
        match self.mode :
            case "IDLE" :
                center_blit(SCREEN,self.rendered_idle,self.pos)
                center_blit(SCREEN,plug_female_idle,(self.pos[0],self.pos[1]+60))
            case "GOOD" :
                center_blit(SCREEN,self.rendered_good,self.pos)
                center_blit(SCREEN,plug_male_good,(self.pos[0]-35,self.pos[1]+60))
                center_blit(SCREEN,plug_female_good,(self.pos[0]+35,self.pos[1]+60))
            case "BAD" :
                center_blit(SCREEN,self.rendered_bad,self.pos)
                if current_frame<3 :
                    center_blit(SCREEN,plug_male_bad,(self.pos[0]-100,self.pos[1]+60))
                    center_blit(SCREEN,plug_female_bad,(self.pos[0]+100,self.pos[1]+60))
                elif current_frame<10 :
                    center_blit(SCREEN,plug_male_bad,(self.pos[0]-100+(current_frame-3)*9,self.pos[1]+60))
                    center_blit(SCREEN,plug_female_bad,(self.pos[0]+100-(current_frame-3)*9,self.pos[1]+60))
            case "CHANGE" :
                center_blit(SCREEN,self.rendered_idle,self.pos)
            case _ :
                center_blit(SCREEN,self.rendered_idle,self.pos)
    def __init__(self,max_frame,num,txt,pos,loop) :
        Anim.__init__(self,max_frame,loop)
        #Engine
        self.num=num
        self.current_num="6"
        self.mode="IDLE"
        self.status="no_con"
        self.txt=txt
        #style
        self.font = pygame.font.Font(NUM_FONT_PATH,NUM_FONT_SIZE)
        #Render
        self.pos=pos
        self.method=self.render
        self.internal_frame=0
        self.rendered_good=self.font.render(self.txt,1,GREEN,COLOR_BG)
        self.rendered_bad=self.font.render(self.txt,1,RED,COLOR_BG)
        self.rendered_idle=self.font.render(self.txt,1,COLOR_HL,COLOR_BG)
    def update(self,value) :
        self.current_num=value
        if self.current_num=="6" :
            self.status="no_con"
            self.mode="IDLE"
        elif self.current_num==self.num :
            self.status="good_con"
            self.mode="GOOD"
        else :
            self.status="bad_con"
            self.mode="BAD"
    def anim(self) :
        Anim.anim(self)

#MAINLOOP PREPARATION
NUMBER_ANIMATIONS=[]
ANIMATIONS=[]

#MAINLOOP
on=True
CLOCK = pygame.time.Clock()
GOOD=0

#Launching thread
thread=arduino.Arduino()
thread.start()

for i,entry in enumerate(texts) :
    NUMBER_ANIMATIONS.append(Number(10,str(i),texts[i],number_pos[i],loop=True))

while on :
    #Cleaning of Screen
    SCREEN.fill(COLOR_BG)

    #Event handling
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            on = False
            thread.on=False
            thread.join()
        if keys[pygame.K_ESCAPE] : # ECHAP : Quitter
            on=False
            thread.on=False
            thread.join()

    #Value update
    arduino_values=thread.get_msg()
    GOOD=0
    for i,entry in enumerate(NUMBER_ANIMATIONS) :
        entry.update(arduino_values[i])
        if entry.status=="good_con" :
            GOOD=GOOD+1

    #Numbers handling
    for i,animation in enumerate(NUMBER_ANIMATIONS) :
        animation.anim()
        if animation.finished :
            NUMBER_ANIMATIONS.pop(i)
    
    #Animation handling
    for i,animation in enumerate(ANIMATIONS) :
        animation.anim()
        if animation.finished :
            ANIMATIONS.pop(i)

    #Show DEBUG
    if DEBUG :
        fps = str(round(CLOCK.get_fps(),1))
        txt = f"DEBUG MODE | FPS : {fps} | GOOD : {GOOD}"
        to_blit=debug_font.render(txt,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,(0,0))

    #End of loop
    pygame.display.update()
    CLOCK.tick(FPS) 