# libraries used here
import customtkinter as ctk
import webbrowser as web

# other scripts
from var_handler import colors, tab, nms

class logTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.placeholder = ctk.CTkLabel(self, text='log tab')
        self.placeholder.grid(row=0,column=0, sticky='ew')