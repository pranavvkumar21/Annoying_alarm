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
    def check_alarms(self):
        pass
    def create_alarm(self):
        pass
    def delete_alarm(self):
        pass


        

# Function to get current volume
def get_current_volume():
    result = subprocess.run(["amixer", "-D", "pulse", "sget", "Master"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Left:' in line:
            # Extract the percentage volume
            print(line)
            volume = line.split()[4].strip('[]%')
            is_mute = line.split()[5    ].strip('[]%')
            return int(volume),is_mute
def unmute():
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "unmute"])

# Function to set volume (takes a percentage as an argument)
def set_volume(volume):
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"])

# Get the current volume
current_volume,is_mute = get_current_volume()
print(f"Current volume: {current_volume}%")
print(is_mute)