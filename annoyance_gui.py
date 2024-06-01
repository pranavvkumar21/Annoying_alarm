#!/usr/bin/env python3
import subprocess
import pygame
import time
import random
import threading
import os
import sys
import tkinter as tk
from tkinter import messagebox

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
pygame.mixer.music.load(default_tune)

def get_current_volume():
    result = subprocess.run(["amixer", "-D", "pulse", "sget", "Master"], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Left:' in line:
            volume = line.split()[4].strip('[]%')
            sound = line.split()[5].strip('[]%')
            return int(volume), sound

def unmute():
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "unmute"])

def set_volume(volume):
    subprocess.run(["amixer", "-D", "pulse", "sset", "Master", f"{volume}%"])

def never_mute(stop_event):
    while not stop_event.is_set():
        try:
            current_volume, sound = get_current_volume()
            if sound == "off":
                unmute()
                set_volume(150)
        except:
            pass

def puzzle_protect():
    rand1 = random.randint(100, 1000)
    rand2 = random.randint(100, 1000)
    rand3 = random.randint(100, 1000)
    answer = rand1 * rand2 * rand3
    correct = 0
    while not correct:
        try:
            response = messagebox.askquestion("Puzzle Protection", f"{rand1} x {rand2} x {rand3}")
            if response == "yes":
                your_answer = simpledialog.askinteger("Input", "Your answer:")
                if your_answer == answer:
                    correct = 1
                    messagebox.showinfo("Success", "Correct answer!")
        except:
            messagebox.showerror("Error", "An error occurred.")
    return correct

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Annoyance App")
        
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack()
        
        self.volume_label = tk.Label(root, text="Current Volume: ")
        self.volume_label.pack()
        
        self.update_volume_label()
        
        self.stop_event = threading.Event()
        self.mute_thread = None
    
    def update_volume_label(self):
        volume, sound = get_current_volume()
        self.volume_label.config(text=f"Current Volume: {volume}%")
        self.root.after(1000, self.update_volume_label)
    
    def start(self):
        pygame.mixer.music.play(loops=-1)
        self.mute_thread = threading.Thread(target=never_mute, args=(self.stop_event,))
        self.mute_thread.start()
        success = puzzle_protect()
        if success:
            self.stop()
    
    def stop(self):
        self.stop_event.set()
        if self.mute_thread:
            self.mute_thread.join()
        pygame.mixer.music.stop()
        messagebox.showinfo("Finished", "Process finished.")
        
root = tk.Tk()
app = App(root)
root.mainloop()
