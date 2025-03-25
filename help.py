import customtkinter as ctk
import os

is_open = False

class helpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # tell the script the window is open
        global is_open
        is_open = True

        # keep the window on top
        self.attributes('-topmost', True)

        # widget init
        self.destroy_button = ctk.CTkButton(self, text='destroy', command=destroy_help_window)

        # widget placement
        self.destroy_button.grid(row=0,column=0, padx=100,pady=100)

def open_help_window(parent):
    # check if the window is already open
    # if not, open the window and set false when closed
    global is_open, window
    if not is_open:
        window = helpWindow(parent)

def destroy_help_window():
    global is_open, window
    if window is not None:
        window.destroy()
        is_open = False