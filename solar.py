# libraries
import customtkinter as ctk
import webbrowser as web
from math import ceil

# import from other scripts
from var_handler import *

def get(input):
    tpc = int(input)
    panels = ceil(tpc/25)           # panels
    batteries = ceil(tpc*800/45000) # min batteries

    # get power generation
    gen_sunrise = gen_sunset = ( panels * 82.5 * 25 )
    gen_day     = panels * 835 * 50
    gen_night   = 0
    gen_total   = gen_sunrise + gen_sunset + gen_day + gen_night

    total_generated = (gen_total) - (tpc * 1000)
    total_power_max = batteries * 45000
    total_power_lost = total_generated - total_power_max
    
    if total_generated > total_power_max:
        batteries_advised = batteries + ceil(total_power_lost / 45000)
    else:
        batteries_advised = None

    return panels, batteries, batteries_advised




class solarTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # register thingy for validation
        self.validate_command=self.register(self.validate)

        # widget config
        self.spacer = ctk.CTkLabel(       self, text='', width=880)
        self.input = ctk.CTkEntry(        self, width=500, height = 50, font=(nms,30), placeholder_text='power consumption (kPs)',
                                  validate='key', validatecommand=(self.validate_command, '%P'))
        self.panel_image = ctk.CTkLabel(  self, text='', image=get_image('solar_panel', 256,256))
        self.panel_label = ctk.CTkLabel(  self, text='Solar Panels:', font=(nms,30), text_color=colors['main'])
        self.panel_indic = ctk.CTkLabel(  self, text='———', font=(nms,30))
        self.battery_image = ctk.CTkLabel(self, text='', image=get_image('battery', 256,256))
        self.battery_label = ctk.CTkLabel(self, text='Batteries:', font=(nms,30), text_color=colors['main'])
        self.battery_label_min = ctk.CTkLabel(self, text='Minimum', font=(nms,20))
        self.battery_label_adv = ctk.CTkLabel(self, text='Advised', font=(nms,20))
        self.battery_indic_min = ctk.CTkLabel(self, text='———', font=(nms,30))
        self.battery_indic_adv = ctk.CTkLabel(self, text='———', font=(nms,30))
        #
        self.dp_credit = ctk.CTkButton(self, text='Based on original code by Devilin Pixy', image=get_image('dp', 50,50), corner_radius=15, fg_color='#8c29e3', hover_color='#6d27ab',
                                       command = lambda: web.open_new_tab('https://jsfiddle.net/DevilinPixy/vm6k1woe/'))
        
        # widget placement
        # hide the adv ones on init and show them if needed
        self.spacer.grid(           row=0,column=0,                     columnspan=2)
        self.input.grid(            row=0,column=0, padx=50,pady=50,    columnspan=2)
        self.panel_image.grid(      row=2,column=0, padx=10,pady=0, sticky='ew')
        self.panel_label.grid(      row=1,column=0, padx=10,pady=0, sticky='ew')
        self.panel_indic.grid(      row=3,column=0,                 sticky='ew')
        self.battery_image.grid(    row=2,column=1, padx=10,pady=0, sticky='ew')
        self.battery_label.grid(    row=1,column=1, padx=10,pady=0, sticky='ew')
        #self.battery_label_min.grid(row=3,column=1,                 sticky='ew')  these are kept for reference
        self.battery_indic_min.grid(row=3,column=1,                 sticky='ew')
        #self.battery_label_adv.grid(row=5,column=1,                 sticky='ew')
        #self.battery_indic_adv.grid(row=6,column=1,                 sticky='ew')
        #
        self.dp_credit.place(x=520, y=630)


    # input validation
    def validate(self,input):
        # if it's a number, allow and calculate
        if input.isdigit() and int(input) <= 99999999999999999999:
            panels, batteries, batteries_adv = get(input) # calculate and get values
            self.update_indics(str(panels), str(batteries), batteries_adv)
            return True
        # check for placeholder text
        elif input == 'power consumption (kPs)':
            return True
        # check for blank
        elif input == '':
            self.update_indics('———','———','———')
            return True
        return False
    
    def update_indics(self, pan, bat, bat_adv):
        # update indic widgets
        self.panel_indic.configure(text=pan)
        self.battery_indic_min.configure(text=bat)
        self.battery_indic_adv.configure(text=bat_adv)

        # check for adv
        if bat_adv is None:
            #hide adv
            self.battery_label_adv.grid_forget()
            self.battery_indic_adv.grid_forget()
            # make min white and remove label
            self.battery_label_min.grid_forget()
            self.battery_indic_min.grid(row=3,column=1, sticky='ew')
            self.battery_label_min.configure(text_color='white')
            self.battery_indic_min.configure(text_color='white')
        else:
            # show adv
            self.battery_label_adv.grid(row=5,column=1, sticky='ew')
            self.battery_indic_adv.grid(row=6,column=1, sticky='ew')
            # show min label and make it grey
            self.battery_label_min.grid(row=3,column=1, sticky='ew')
            self.battery_indic_min.grid(row=4,column=1, sticky='ew')
            self.battery_label_min.configure(text_color='#A1A1A1')
            self.battery_indic_min.configure(text_color='#A1A1A1')