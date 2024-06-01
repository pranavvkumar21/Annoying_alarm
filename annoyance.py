#!/usr/bin/env python3
import subprocess
import pygame
import time
import random
import simpleaudio
import threading

import os
import sys

# Function to redirect stdout and stderr temporarily
class HideOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

# Use the context manager to hide output during pygame.mixer initialization
with HideOutput():
    pygame.mixer.init()

default_tune = "./sounds/beep1.wav"


# Load the music file
with HideOutput():
    pygame.mixer.music.load(default_tune)
def get_current_volume():
    result = subprocess.run(["amixer", "-D", "pulse", "sget", "Master"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Left:' in line:
            # Extract the percentage volume
            #print(line)
            volume = line.split()[4].strip('[]%')
            sound = line.split()[5].strip('[]%')
            return int(volume),sound
def unmute():
    with HideOutput():
        a = subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "unmute"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to set volume (takes a percentage as an argument)
def set_volume(volume):
    with HideOutput():
        a =subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Get the current volume

def never_mute(stop_event):
    
    while not stop_event.is_set():
        try:
            
            current_volume,sound = get_current_volume()
            if sound == "off":
                unmute()
                set_volume(150)
        except KeyboardInterrupt:
            pass
        except:
            pass

def puzzle_protect():
    rand1 = random.randint(1,10)
    rand2 = random.randint(1,10)
    rand3 = random.randint(1,10)
    answer = rand1*rand2*rand3
    correct = 0
    while not correct:
        try:
            print(f"{rand1} x {rand2} x {rand3}")
            your_answer = input("your answer: ")
            if int(your_answer) == answer:
                correct = 1
                print("yaaay")
            else:
                print("try again!\n")
        except KeyboardInterrupt:
            print("\n no use trying to do that")
        except:
            print("wrong answer")
            print("try again!\n")
    return correct


stop_event = threading.Event()
for i in range(1):
    with HideOutput():
        pygame.mixer.music.play(loops=-1)
    mute_thread = threading.Thread(target=never_mute, args=(stop_event,))
    mute_thread.start()
    success = puzzle_protect()
    stop_event.set()
    mute_thread.join()
    print("finishedd")
    time.sleep(0.2)