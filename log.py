# libraries used here
import customtkinter as ctk
import webbrowser as web

# other scripts
from var_handler import colors, tab, nms

class logTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # WIDGETS
        self.spacer = ctk.CTkLabel(self, text='', width=880)
        
        # PLACEMENT
        self.spacer.grid(row=0,column=0, sticky='ew')