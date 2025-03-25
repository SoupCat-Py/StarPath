# libraries used here
import customtkinter as ctk
import webbrowser as web

# other scripts
from var_handler import colors, tab, nms

class glyphTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.placeholder = ctk.CTkLabel(self, text='glyph tab')
        self.placeholder.grid(row=0,column=0, sticky='ew')