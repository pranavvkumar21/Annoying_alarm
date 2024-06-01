#!/usr/bin/env python3
import subprocess
import pygame
import datetime
# Initialize the mixer module in pygame

default_tune = "your_music_file.mp3"
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load("your_music_file.mp3")


class Alarm():
    def __init__(self,label,time,repeat,tune=default_tune):
        self.label = label
        self.hour,self.minutes = time.split(":")
        self.repeat = repeat
        self.tune = tune

class annoying_alarm():
    def __init__(self,tune = default_tune):
        self.alarms = {}
    
    def create_alarm(self):
        pass
    def delete_alarm(self):
        pass
    def check_alarms(self):
        pass
    def ring_alram(self):
        pass
    def the_annoying_bit(self):
        pass



        