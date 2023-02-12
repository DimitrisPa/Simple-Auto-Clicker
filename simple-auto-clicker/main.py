#!/usr/bin/env python

import customtkinter
import os
from pynput import keyboard
from pynput.keyboard import Listener
from pynput.mouse import Button, Controller
import threading
import time
import tkinter

# Hotkey F6
TOGGLE_KEY = keyboard.Key.f6

running = False
thread = None

# Default click speed value
clicks_ps = 10

# Detect mouse.ico path
icon_path = os.path.join(os.path.dirname(__file__), "mouse_circle.png")


# Clicks per second input
def cps(event=None):
    global clicks_ps
    if entry.get() == "":
        entry.delete(0, "end")
        entry.insert(0, "Clicks per second")
        entry.configure(text_color="#9e9e9e")
    else:
        clicks_ps = int(entry.get())
        entry.delete(0, "end")
        entry.insert(0, "Clicks per second")
        entry.configure(text_color="#9e9e9e")


# Remove Placeholder_text on input
def clear_placeholder_on_input(event):
    if entry.get() == "Clicks per second":
        entry.delete(0, "end")


# Restore Placeholder_text on click
def clear_placeholder_on_focus_out(event):
    if entry.get() == "":
        entry.insert(0, "Clicks per second")
        entry.configure(text_color="#9e9e9e")


# Left Click
def clicking():
    mouse = Controller()
    while running:
        if running:
            mouse.click(Button.left)
            time.sleep(1/clicks_ps)


# Press function for button
def press():
    global running, thread
    if not running:
        time.sleep(1)
        running = True
        thread = threading.Thread(target=clicking)
        thread.start()


# Hotkey press function
def toggle_key(key):
    global running, thread
    if key == TOGGLE_KEY:
        if running:
            running = False
            thread.join()
        else:
            press()
            print("Hotkey pressed")


# Listener function
def start_l():
    with Listener(on_press=toggle_key) as listener:
        listener.join()


# Thread for start_l function
l_thread = threading.Thread(target=start_l)
l_thread.start()


# CustomTkinter theme
app = customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# GUI Layout
app.geometry("300x250")
app.resizable(0, 0)
app.iconphoto(True, tkinter.PhotoImage(file=icon_path))
app.title("Simple Auto Clicker")

frame = customtkinter.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label = customtkinter.CTkLabel(
    master=frame, text="Simple Auto Clicker", font=("Carlito", 16, "bold"))
label.pack(pady=10, padx=10)

on_off_button = customtkinter.CTkButton(
    master=frame, text="On / Off (F6)", font=("Carlito", 16), command=lambda: press())
on_off_button.pack(pady=10, padx=10)

entry = customtkinter.CTkEntry(
    master=frame, placeholder_text="Clicks per second")
entry.configure(font=("Carlito", 16), justify="center")
entry.pack(pady=10, padx=10)
entry.bind("<Key>", clear_placeholder_on_input)
entry.bind(command=cps)

app.bind("<Button-1>", clear_placeholder_on_focus_out)
app.bind("<Return>", cps)
app.bind("<KP_Enter>", cps)

submit_button = customtkinter.CTkButton(
    master=frame, text="Change", font=("Carlito", 16), command=cps)
submit_button.pack(pady=10, padx=10)

app.mainloop()
