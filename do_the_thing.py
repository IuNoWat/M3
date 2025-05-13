#!/usr/bin/python
#coding: utf-8

import time

import pygame
from pygame.locals import *
pygame.init()
pygame.font.init()

import arduino_serial as arduino

#CONSTANTS
FPS=30
SCREEN_SIZE=(1600, 900)
FULLSCREEN=True

#ASSETS


#COLORS
WHITE=pygame.Color("White")
BLACK=pygame.Color("Black")
COLOR_BG=pygame.Color(22,13,34,255)
COLOR_HL=pygame.Color(255,255,255,255)

#POSITION OF NUMBERS


#NUMBER CLASS
class Number() :
    def __init__(self,pos,analogEntry) :
        self.pos=pos
        self.analogEntry=analogEntry
        self.value=False
        #Style des nombres
        self.font = pygame.font.Font(NUM_FONT_PATH,font_size)
    def render(self) :
        self.value=arduino.get_arduino_info()[self.analogEntry]
        return self.font.render(formated_value,1,COLOR_HL,COLOR_BG)



#MAINLOOP PREPARATION
running=True
SCREEN = pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN)
CLOCK = pygame.time.Clock()

#MAINLOOP
while running :
    #Cleaning of Screen
    SCREEN.blit

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed() :
            running = False
    
    #End of loop
    pygame.display.flip()
    CLOCK.tick(FPS)

