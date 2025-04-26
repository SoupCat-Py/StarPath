# libraries used here
import customtkinter as ctk
import webbrowser as web
import math
import tkinter.messagebox as msg
from decimal import Decimal

# other scripts
from var_handler import colors, tab, nms, get_image, left_click

# string for step 2 to make it less cluttered
step2_text = '''
⬇

Travel at least 1000u

⬇

Step 2:'''

# gradient from red to grey
fade = ["#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#ff0000", "#f2281d", "#d94436", "#bf5447", "#a45e54", "#88655f", "#696969"]



def calculate(lat1,lat2,long1,long2,dist):
    # magic formula
    laylineDistance = (655*math.sqrt((lat2-lat1)**2 + (long2-long1)**2)) / dist

    # get actual laylines
    angles = [-90, 0, 90, 180]
    listAdd = [angle + (laylineDistance/2) for angle in angles]
    listSubtract = [angle - (laylineDistance/2) for angle in angles]

    # combine
    listResult = listAdd + listSubtract

    # check for out of range
    for i in range (len(listResult)):
        if listResult[i] > 180:
            listResult[i] -= 360
        if listResult[i] < -180:
            listResult[i] += 360
        # round
        listResult[i] = round(listResult[i], 2)

    # cleanup and return
    listResult.sort()
    listResult.reverse()
    verticalResult = "\n".join(map(str, listResult))
    return verticalResult


# frame for the result
class resultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # frame config
        self._corner_radius=25
        self._border_color=colors['main']
        self._border_width=4

        # config
        self.result_title = ctk.CTkLabel(self, text='Laylines at these longitudes:', font=(nms,30))
        self.result_label = ctk.CTkLabel(self, text=('\n' * 7), font=('Arial',25))

        # placement
        self.result_title.grid(row=0,column=0, padx=20,pady=20, sticky='ew')
        self.result_label.grid(row=1,column=0, padx=10,pady=20, sticky='nsew')


# main frame for layline tab
class laylineTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # VALIDATION
        self.vc_f = self.register(self.validate_float)   # for lats and longs
        self.vc_d = self.register(self.validate_integer) # for distance

        # WIDGET INIT
        #   spacer
        self.spacer = ctk.CTkLabel(self, text='', width=880, height=100)
        #   inputs
        self.step1 =       ctk.CTkLabel(self, text='Step 1:', text_color='#AAAAAA', font=(nms,20))
        self.lat1_entry =  ctk.CTkEntry(self, placeholder_text='lat',      width=130, font=(nms,30), border_color='#696969', validate='key', validatecommand=(self.vc_f,'%P','%W'), justify='center')
        self.long1_entry = ctk.CTkEntry(self, placeholder_text='long',     width=130, font=(nms,30), border_color='#696969', validate='key', validatecommand=(self.vc_f,'%P','%W'), justify='center')
        self.step2 =       ctk.CTkLabel(self, text=step2_text, text_color='#AAAAAA', font=(nms,20))
        self.lat2_entry =  ctk.CTkEntry(self, placeholder_text='lat',      width=130, font=(nms,30), border_color='#696969', validate='key', validatecommand=(self.vc_f,'%P','%W'), justify='center')
        self.long2_entry = ctk.CTkEntry(self, placeholder_text='long',     width=130, font=(nms,30), border_color='#696969', validate='key', validatecommand=(self.vc_f,'%P','%W'), justify='center')
        self.dist_entry =  ctk.CTkEntry(self, placeholder_text='distance', width=270, font=(nms,30), border_color='#696969', validate='key', validatecommand=(self.vc_d,'%P'), justify='center')
        #self.locate =     ctk.CTkButton(self, text='Locate', font=(nms,30), width=250, height=60, command=self.send_inputs,
        #                                image=get_image('locate',40,40), corner_radius=20)
        self.locate =      ctk.CTkLabel(self, text='', image=get_image('locate_norm',250,50))
        self.clear =      ctk.CTkButton(self, text='Clear', command=self.clear_inputs,
                                        text_color='red', fg_color='transparent', hover_color=colors['dark'], border_width=3, border_color='red')
        #   output
        self.result_frame = resultFrame(self)
        #   other
        self.nmslc_button = ctk.CTkLabel(self, text='', image=get_image('nmslc_norm',70,70), width=0, height=0)
        self.video_button = ctk.CTkButton(self, text='Video Guide', width=200, height=40,
                                          fg_color=colors['main'], hover_color=colors['dark'], image=get_image('yt',30,30), corner_radius=50,
                                          command=lambda: web.open_new_tab('https://www.youtube.com/watch?v=Ec8QN39GNB8'))
        

        # WIDGET PLACEMENT
        #   spacer
        self.spacer.grid     (row=0,column=0,                  sticky='ew', columnspan=3)
        #   inputs
        self.step1.grid      (row=0,column=0,                  sticky='sew', columnspan=2)
        self.lat1_entry.grid (row=1,column=0, padx=5,pady=10,  sticky='e')
        self.long1_entry.grid(row=1,column=1, padx=5,pady=10,  sticky='w')
        self.step2.grid      (row=2,column=0,                  sticky='ew', columnspan=2)
        self.lat2_entry.grid (row=3,column=0, padx=5,pady=10,  sticky='e')
        self.long2_entry.grid(row=3,column=1, padx=5,pady=10,  sticky='w')
        self.dist_entry.grid (row=4,column=0, padx=10,pady=10,              columnspan=2)
        self.locate.grid     (row=6,column=0, pady=40,         sticky='ns', columnspan=2)
        self.clear.grid      (row=5,column=0,                  sticky='ns', columnspan=2)
        #   result
        self.result_frame.grid(row=1,column=2, padx=20,pady=20, rowspan=5)
        #   other
        self.nmslc_button.place(x=800, y=640)
        self.video_button.place(x=590, y=655)

        # KEYBINDS
        self.locate.bind('<Enter>',  lambda e: self.locate.configure(image=get_image('locate_hov', 250,50)))
        self.locate.bind('<Leave>',  lambda e: self.locate.configure(image=get_image('locate_norm',250,50)))
        self.locate.bind(left_click, lambda e: self.send_inputs())
        #
        self.nmslc_button.bind('<Enter>',  lambda e: self.nmslc_button.configure(image=get_image('nmslc_hov',70,70)))
        self.nmslc_button.bind('<Leave>',  lambda e: self.nmslc_button.configure(image=get_image('nmslc_norm',70,70)))
        self.nmslc_button.bind(left_click, lambda e: web.open_new_tab('https://github.com/SoupCat-Py/NMS-Layline-Calculator'))


    def validate_integer(self,input):
        # check for digit and make sure it fits in the entry
        if input.isdigit() and int(input) < 99999999999999:
            return True
        # check for blank or placeholder
        elif input == '' or input == 'distance':
            return True
        return False
    
    def validate_float(self, input, widget):
        # check for lone hyphen, blank, placeholder
        if input == '-' or input == '' or input in ['lat','long']:
            return True
        else:
            # check for float
            try:
                input = float(input)

                # check for decimal precision
                decimal = Decimal(str(input))
                if abs(decimal.as_tuple().exponent) > 2:
                    self.glow_red(widget)
                    return False
                # check for range
                # -90 to 90 for lat, -180 to 180 for long
                if widget in [f'{self.lat1_entry}.!entry', f'{self.lat2_entry}.!entry']:     # lat
                    self.glow_red(widget) if input > 90 or input < -90 else None             # initiate glow if out of range
                    return True if -90 <= input <= 90 else False                             # return true if in range - false if out
                elif widget in [f'{self.long1_entry}.!entry', f'{self.long2_entry}.!entry']: # long
                    self.glow_red(widget) if input > 180 or input < -180 else None           # initiate glow if out of range
                    return True if input -180 <= input <= 180 else False                     # return true if in range - false if not
            except ValueError:
                return False
        return False
    

    def fade_back(self, entry):
        if self.fade_stage < len(fade):
            entry.configure(border_color=fade[self.fade_stage])
            self.fade_stage += 1
            entry.after(50, lambda: self.fade_back(entry))
    
    def glow_red(self, input_entry):
        entry_name = self.nametowidget(input_entry)  # get name of focused entry - from string to widget
        parent_entry = entry_name.winfo_parent()     # get parent of the new widget - remove .!entry
        entry = self.nametowidget(parent_entry)      # get name of parent entry

        self.fade_stage = 0                    # set starting point for fade_back
        self.fade_back(entry)                  # start the fading loop

    def clear_inputs(self):
        # check all inputs
        for input in [self.lat1_entry,self.lat2_entry,self.long1_entry,self.long2_entry,self.dist_entry]:
            # clear if not empty to keep placeholder
            input.delete(0,ctk.END) if input.get() != '' else None

    def send_inputs(self):
        # get values
        lat1_temp =  self.lat1_entry.get()
        long1_temp = self.long1_entry.get()
        lat2_temp =  self.lat2_entry.get()
        long2_temp = self.long2_entry.get()
        dist_temp =  self.dist_entry.get()

        # make sure they're all filled
        if lat1_temp != '' and long1_temp != '' and lat2_temp != '' and long2_temp != '' and dist_temp != '':
            # calculate values and update results
            self.result_frame.result_label.configure(text=calculate(float(lat1_temp), float(lat2_temp), float(long1_temp), float(long2_temp), float(dist_temp)))
        else:
            # show user an error
            msg.showinfo('error','Please make sure all the inputs are filled out 😉')