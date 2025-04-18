# libraries used here
import customtkinter as ctk
import tkinter.messagebox as msg
import webbrowser as web

# other scripts
from var_handler import *

def save_data(data):
    with open(log_file, 'w') as file:
        # write data to the json file
        # indent makes easier readability
        json.dump(data, file, indent=4)
        
def load_data():
    try:  # in case the file doesn't exist
        with open(log_file, 'r') as file:
            try:
                # load data from the json file
                return json.load(file)
            except json.decoder.JSONDecodeError:   # in case file is empty
                return []
    except FileNotFoundError:
        # return empty if the file doesn't exist
        return []
    

class entries(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

class logTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # frame config
        self.grid_columnconfigure([0], weight=3)
        self.grid_columnconfigure([1], weight=1)
        
        # validation
        self.vc_h = self.register(self.validate_hex)
        self.vc_o = self.register(self.validate_other)

        # WIDGETS
        self.spacer = ctk.CTkLabel(self, text='', width=880)
        self.input_title  = ctk.CTkEntry(self, width=600, font=(nms,20), validate='key', validatecommand=(self.vc_o, '%P','title'),  placeholder_text='Title')
        self.input_desc   = ctk.CTkEntry(self, width=600, font=(nms,20), validate='key', validatecommand=(self.vc_o, '%P','desc'),   placeholder_text='Description/Note')
        self.input_hex    = ctk.CTkEntry(self, width=600, font=(nms,20), validate='key', validatecommand=(self.vc_h, '%P'),          placeholder_text='Address')
        self.input_galaxy = ctk.CTkEntry(self, width=600, font=(nms,20), validate='key', validatecommand=(self.vc_o, '%P','galaxy'), placeholder_text='Galaxy')
        self.input_type     = ctk.CTkOptionMenu(self, width=200, values=['Star Colour',     'Yellow', 'Red', 'Green', 'Blue', 'Purple'])
        self.input_econ     = ctk.CTkOptionMenu(self, width=200, values=['Economy Rating',  '⭐️','⭐️⭐️','⭐️⭐️⭐️','Outlaw'])
        self.input_econtype = ctk.CTkOptionMenu(self, width=200, values=['Economy Type',    'Scientific','Trading','Advanced Materials','Power Production','Manufacturing','Mining','Technology'])
        self.create_button = ctk.CTkButton(self, text='Create Log Entry', font=(nms,20), fg_color=colors['blue-m'], corner_radius=20, command=self.create_entry)
        
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
        self.create_button.grid( row=4,column=1, padx=20,pady=5, sticky='nsew')
        
        self.entry_data = load_data()
        self.entry_list = []
        
        
    def validate_hex(self, final_input):
        # allow blank or placeholder
        if final_input in ['','Address']:
            return True
        elif len(final_input) <= 12:
            try:
                int(final_input, 16)
                return True
            except:
                return False
        return False
    
    def validate_other(self, final_input, type):
        limit = 50 if type == 'desc' else 30
        if len(final_input) <= limit:
            return True
        return False
    
    def create_entry(self):
        
        #
        
        # delete all input fields
        for text_input in (self.input_title, self.input_desc, self.input_hex, self.input_galaxy):
            text_input.delete(0, ctk.END) if text_input.get() != '' else None
        self.input_type.set('Star Colour')
        self.input_econ.set('Economy Rating')
        self.input_econtype.set('Economy Type')
        # remove focus
        self.spacer.focus_set()
    
    # TODO: add "msg.askyesno" if address is under 12 characters when user presses "create"