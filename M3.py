import sys
import random
import time
import os

import pygame
pygame.init()

from tools import *
import arduino_serial as arduino

#CONSTANTS
FPS=30
DIR=os.getcwd()+"/"
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

#GAMEPLAY
txt=[
    "39 kWh",
    "49 kWh",
    "131 kWh",
    "162 kWh",
    "301 kWh",
    "346 kWh"
]

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
elec=pygame.transform.scale_by(pygame.image.load(DIR+"M3/assets/elec.png").convert_alpha(),0.2)

#STYLE
WHITE=pygame.Color("White")
BLACK=pygame.Color("Black")
GREEN=pygame.Color("Green")
RED=pygame.Color("Red")
COLOR_BG=pygame.Color(22,13,34,255)
COLOR_HL=pygame.Color(255,255,255,255)

NUM_FONT_SIZE=70
FONT_STYLE=NUM_FONT_PATH
FONT_COLOR=COLOR_HL

pygame.font.init()
debug_font=pygame.font.Font(TXT_FONT_PATH,16)
num_font = pygame.font.Font(NUM_FONT_PATH,NUM_FONT_SIZE)

rendered_good=[
    num_font.render(txt[0],1,GREEN,COLOR_BG),
    num_font.render(txt[1],1,GREEN,COLOR_BG),
    num_font.render(txt[2],1,GREEN,COLOR_BG),
    num_font.render(txt[3],1,GREEN,COLOR_BG),
    num_font.render(txt[4],1,GREEN,COLOR_BG),
    num_font.render(txt[5],1,GREEN,COLOR_BG),
]

rendered_bad=[
    num_font.render(txt[0],1,RED,COLOR_BG),
    num_font.render(txt[1],1,RED,COLOR_BG),
    num_font.render(txt[2],1,RED,COLOR_BG),
    num_font.render(txt[3],1,RED,COLOR_BG),
    num_font.render(txt[4],1,RED,COLOR_BG),
    num_font.render(txt[5],1,RED,COLOR_BG),
]

rendered_idle=[
    num_font.render(txt[0],1,COLOR_HL,COLOR_BG),
    num_font.render(txt[1],1,COLOR_HL,COLOR_BG),
    num_font.render(txt[2],1,COLOR_HL,COLOR_BG),
    num_font.render(txt[3],1,COLOR_HL,COLOR_BG),
    num_font.render(txt[4],1,COLOR_HL,COLOR_BG),
    num_font.render(txt[5],1,COLOR_HL,COLOR_BG),
]

#POSITION OF NUMBERS

uper_left_corner=(5,16)
lower_right_corner=(1902,230)

rect_height=215
rect_width=300

y_offset = 840
x_offset = 15
#POSITIONS ABSOLUES

number_pos=[
    (x_offset + 160  , y_offset + rect_height/2),
    (x_offset + 480  , y_offset + rect_height/2),
    (x_offset + 800  , y_offset + rect_height/2),
    (x_offset + 1120 , y_offset + rect_height/2),
    (x_offset + 1440 , y_offset + rect_height/2),
    (x_offset + 1760 , y_offset + rect_height/2),
]

number_rect=[
    pygame.Rect((number_pos[0][0]-rect_width/2,number_pos[0][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((number_pos[1][0]-rect_width/2,number_pos[1][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((number_pos[2][0]-rect_width/2,number_pos[2][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((number_pos[3][0]-rect_width/2,number_pos[3][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((number_pos[4][0]-rect_width/2,number_pos[4][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((number_pos[5][0]-rect_width/2,number_pos[5][1]-rect_height/2),(rect_width,rect_height)),
]

#POSITIONS ALIGNEES


real_pos=[
    (x_offset + 160  -5 , y_offset + rect_height/2 +14),
    (x_offset + 480  -5 , y_offset + rect_height/2 +15),
    (x_offset + 800  -8,  y_offset + rect_height/2 +18),
    (x_offset + 1120 -11, y_offset + rect_height/2 +20),
    (x_offset + 1440 -13 ,y_offset + rect_height/2 +23),
    (x_offset + 1760 -13 ,y_offset + rect_height/2 +24),
]

number_rect_real=[
    pygame.Rect((real_pos[0][0]-rect_width/2,real_pos[0][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((real_pos[1][0]-rect_width/2,real_pos[1][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((real_pos[2][0]-rect_width/2,real_pos[2][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((real_pos[3][0]-rect_width/2,real_pos[3][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((real_pos[4][0]-rect_width/2,real_pos[4][1]-rect_height/2),(rect_width,rect_height)),
    pygame.Rect((real_pos[5][0]-rect_width/2,real_pos[5][1]-rect_height/2),(rect_width,rect_height)),
]

#ANIM CONSTANT
Y_OF_PLUG=50
Y_OF_NUM=-50

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
        center_blit(SCREEN,self.img,(self.pos[0],self.pos[1]-current_frame*5))
    def __init__(self,max_frame,img,pos) :
        Anim.__init__(self,max_frame)
        self.img=img
        self.pos=pos
        self.method=self.moove
    def anim(self) :
        Anim.anim(self)

class Translate_ball(Anim) :
    def moove(self,current_frame) :
        pygame.draw.circle(SCREEN,self.color,(self.pos[0]-self.width/2+self.jump_by_frame*self.current_frame,self.pos[1]),self.size)
    def __init__(self,max_frame,pos,width,size=15,color=GREEN) :
        Anim.__init__(self,max_frame)
        self.pos=pos
        self.width=width
        self.color=color
        self.size=size
        self.method=self.moove
        self.jump_by_frame=width/max_frame
    def anim(self) :
        Anim.anim(self)    

#SPECIFIC ENGINE

class Number(Anim) : # The Numbers (the values stored in txt) are shown as a specific Anim subclass stored in a specific list : NUMBER_ANIMATIONS
    def render(self,current_frame) :
        global ANIMATIONS
        if self.old_mode!=self.mode :
            self.current_frame=0
        self.old_mode=self.mode
        match self.mode :
            case "IDLE" :
                center_blit(SCREEN,rendered_idle[int(self.num)],(self.pos[0],self.pos[1]+Y_OF_NUM))
                center_blit(SCREEN,plug_female_idle,(self.pos[0],self.pos[1]+Y_OF_PLUG))
            case "GOOD" :
                center_blit(SCREEN,rendered_good[int(self.num)],(self.pos[0],self.pos[1]+Y_OF_NUM))
                center_blit(SCREEN,plug_male_good,(self.pos[0]-35,self.pos[1]+Y_OF_PLUG))
                center_blit(SCREEN,plug_female_good,(self.pos[0]+35,self.pos[1]+Y_OF_PLUG))
                pygame.draw.line(SCREEN,GREEN,(self.pos[0]-rect_width/2,self.pos[1]+Y_OF_PLUG),(self.pos[0]+rect_width/2,self.pos[1]+Y_OF_PLUG),8)
                if current_frame==0 and VICTORY_PLAYING==False :
                    ANIMATIONS.append(Translate_ball(30,(self.pos[0],self.pos[1]+Y_OF_PLUG),rect_width))
            case "BAD" :
                center_blit(SCREEN,rendered_bad[int(self.num)],(self.pos[0],self.pos[1]+Y_OF_NUM))
                if current_frame<3 :
                    center_blit(SCREEN,plug_male_bad,(self.pos[0]-100,self.pos[1]+Y_OF_PLUG))
                    center_blit(SCREEN,plug_female_bad,(self.pos[0]+100,self.pos[1]+Y_OF_PLUG))
                elif current_frame<10 :
                    center_blit(SCREEN,plug_male_bad,(self.pos[0]-100+(current_frame-3)*9,self.pos[1]+Y_OF_PLUG))
                    center_blit(SCREEN,plug_female_bad,(self.pos[0]+100-(current_frame-3)*9,self.pos[1]+Y_OF_PLUG))
            case "CHANGE" :
                center_blit(SCREEN,rendered_good[int(self.num)],(self.pos[0],self.pos[1]+Y_OF_NUM))
                center_blit(SCREEN,plug_male_good,(self.pos[0]-35,self.pos[1]+Y_OF_PLUG))
                center_blit(SCREEN,plug_female_good,(self.pos[0]+35,self.pos[1]+Y_OF_PLUG))
                pygame.draw.line(SCREEN,GREEN,(self.pos[0]-rect_width/2,self.pos[1]+Y_OF_PLUG),(self.pos[0]+rect_width/2,self.pos[1]+Y_OF_PLUG),8)
                pygame.draw.circle(SCREEN,GREEN,self.pos,self.current_frame*23)
            case _ :
                center_blit(SCREEN,self.rendered_idle,self.pos)
    def __init__(self,max_frame,num,pos,loop) :
        Anim.__init__(self,max_frame,loop)
        #Engine
        self.num=num
        self.current_num="6"
        self.mode="IDLE"
        self.old_mode="IDLE"
        self.status="no_con"
        #Render
        self.pos=pos
        self.method=self.render
        self.internal_frame=0
    def update(self,value) :
        global VICTORY_PLAYING
        self.current_num=value
        if VICTORY_PLAYING and VICTORY_ANIM_TIMER<10 :
            self.mode="CHANGE"
        else :
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
VICTORY_TIMER=0
VICTORY_ANIM_TIMER=0
VICTORY_PLAYING=False

debug_pos=[0,0]

#Launching thread
thread=arduino.Arduino()
thread.start()

for i,entry in enumerate(txt) :
    NUMBER_ANIMATIONS.append(Number(10,str(i),real_pos[i],loop=True))

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
    
    #Victory handling
    if GOOD==6 and VICTORY_PLAYING==False:
        VICTORY_TIMER+=1
        if VICTORY_TIMER>15 :
            #TOOD launch animation
            VICTORY_PLAYING=True
            ANIMATIONS=[]
            ANIMATIONS.append(Translate_ball(60,(1920/2,real_pos[2][1]+Y_OF_PLUG),1920,40))
            VICTORY_ANIM_TIMER=70
    else :
        VICTORY_TIMER=0

    if VICTORY_PLAYING :
        if VICTORY_ANIM_TIMER==0 :
            VICTORY_PLAYING=False
            to_give=["0","1","2","3","4","5"]
            for i,number in enumerate(NUMBER_ANIMATIONS) :
                new_number=random.choice(to_give)
                if i!=0 :
                    while new_number==number.num :
                        print(f"{i} - {to_give}")
                        new_number=random.choice(to_give)
                else :
                    new_number=NUMBER_ANIMATIONS[5].num
                number.num=new_number
                to_give.remove(new_number)
        else :
            VICTORY_ANIM_TIMER=VICTORY_ANIM_TIMER-1

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
        #Show Cursor
        keys = pygame.key.get_pressed()
        to_ad=1
        if keys[pygame.K_SPACE] :
            to_ad=15
        if keys[pygame.K_UP] :
            debug_pos[1]=debug_pos[1]-to_ad
        if keys[pygame.K_DOWN] :
            debug_pos[1]=debug_pos[1]+to_ad
        if keys[pygame.K_LEFT] :
            debug_pos[0]=debug_pos[0]-to_ad
        if keys[pygame.K_RIGHT] :
            debug_pos[0]=debug_pos[0]+to_ad 
        pos=f"{debug_pos[0]},{debug_pos[1]}"
        to_blit=debug_font.render(pos,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,debug_pos)
        SCREEN.set_at(debug_pos,WHITE)
        #Show Rects
        for pos in number_pos :
            pygame.draw.line(SCREEN,WHITE,(pos[0],pos[1]-rect_height/2),(pos[0],pos[1]+rect_height/2))
            pygame.draw.line(SCREEN,WHITE,(pos[0]-rect_width/2,pos[1]),(pos[0]+rect_width/2,pos[1]))
        for entry in number_rect :
            pygame.draw.rect(SCREEN,WHITE,entry,1)
        for pos in real_pos :
            pygame.draw.line(SCREEN,RED,(pos[0],pos[1]-rect_height/2),(pos[0],pos[1]+rect_height/2))
            pygame.draw.line(SCREEN,RED,(pos[0]-rect_width/2,pos[1]),(pos[0]+rect_width/2,pos[1]))
        for entry in number_rect_real :
            pygame.draw.rect(SCREEN,RED,entry,1)
        #Show FPS
        fps = str(round(CLOCK.get_fps(),1))
        txt = f"DEBUG MODE | FPS : {fps} | GOOD : {GOOD} | ARDUINO : {arduino_values} | VICTORY_TIMER : {VICTORY_TIMER} | VICTORY_ANIM_TIMER : {VICTORY_ANIM_TIMER}"
        to_blit=debug_font.render(txt,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,(0,0))

    #End of loop
    pygame.display.update()
    CLOCK.tick(FPS) 