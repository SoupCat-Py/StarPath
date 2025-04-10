# libraries used here
import customtkinter as ctk
import webbrowser as web

# other scripts
from var_handler import *

def write_data(data, file):
    pass

class logTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # frame config
        self.grid_columnconfigure([0], weight=3)
        self.grid_columnconfigure([1], weight=1)

        # WIDGETS
        self.spacer = ctk.CTkLabel(self, text='', width=880)
        self.input_title  = ctk.CTkEntry(self, width=600, placeholder_text='Title', font=(nms,20))
        self.input_desc   = ctk.CTkEntry(self, width=600, placeholder_text='Description/Note', font=(nms,20))
        self.input_hex    = ctk.CTkEntry(self, width=600, placeholder_text='Address', font=(nms,20))
        self.input_galaxy = ctk.CTkEntry(self, width=600, placeholder_text='Galaxy', font=(nms,20))
        self.input_type     = ctk.CTkOptionMenu(self, width=200, values=['Star Colour',     'Yellow', 'Red', 'Green', 'Blue', 'Purple'])
        self.input_econ     = ctk.CTkOptionMenu(self, width=200, values=['Economy Rating',  '⭐️','⭐️⭐️','⭐️⭐️⭐️','Outlaw'])
        self.input_econtype = ctk.CTkOptionMenu(self, width=200, values=['Economy Type',    'Scientific','Trading','Advanced Materials','Power Production','Manufacturing','Mining','Technology'])
        
        # set all the colours like this because i'm lazy and it would look terrible otherwise
        for optionmenu in [self.input_type, self.input_econ, self.input_econtype]:
            optionmenu.configure(fg_color=colors['main'], button_color=colors['dark'], button_hover_color=colors['light'])
        
        # PLACEMENT
        self.spacer.grid(row=0,column=0, sticky='ew', columnspan=2)
        #
        self.input_title.grid(   row=1,column=0, padx=20,pady=5, sticky='nsew')
        self.input_desc.grid(    row=2,column=0, padx=20,pady=5, sticky='nsew')
        self.input_hex.grid(     row=3,column=0, padx=20,pady=5, sticky='nsew')
        self.input_galaxy.grid(  row=4,column=0, padx=20,pady=5, sticky='nsew')
        self.input_type.grid(    row=1,column=1, padx=20,pady=5, sticky='nsew')
        self.input_econ.grid(    row=2,column=1, padx=20,pady=5, sticky='nsew')
        self.input_econtype.grid(row=3,column=1, padx=20,pady=5, sticky='nsew')
        
        
        # if address is not 12 characters, warn the user but let them proceed
        # set the fg color of the frame to be the star type
        # example layout:
        '''ENTRY NAME
           0123456789AB • Euclid'''