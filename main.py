# libraries used in here
import customtkinter as ctk     # GUI
import tkinter as tk
import os                       # system stuff
from PIL import Image as image  # images
import webbrowser as web        # opening wiki

# import from other scripts
from var_handler import *
from solar import solarTab
from layline import laylineTab
from glyph import glyphTab
from log import logTab
from settings import settingsTab

# remember do make a folder in either User or AppData for images
# then reroute there

class sidebarFrame(ctk.CTkFrame):
    #initialization
    def __init__(self, master):
        super().__init__(master)

        # frame config
        self.grid_propagate(False)          # prevent grid placement from resizing
        self.columnconfigure(0, weight=1)   # make the column expand the width of the sidebar
        self.configure(width=200, height=720, 
                       fg_color=colors['main'],
                       corner_radius=0)
        
        # widget config
        self.sidebar_title =  ctk.CTkButton(self, text='StarPath', font=(nms,30), hover=False, fg_color=colors['main'])
        self.solar_button =   ctk.CTkLabel( self, text='', image=get_image('solar_norm', 180,60))
        self.layline_button = ctk.CTkLabel( self, text='', image=get_image('layline_norm', 180,60))
        self.glyph_button =   ctk.CTkLabel( self, text='', image=get_image('glyph_norm', 180,60))
        self.log_button =     ctk.CTkLabel( self, text='', image=get_image('log_norm', 180,60))
        self.settings_button =ctk.CTkButton(self, text='Settings', fg_color=colors['dark'], hover_color=colors['accent'], corner_radius=15, command=self.open_settings)
        self.help =           ctk.CTkButton(self, text='Help', font=(nms, 15), width=50, command = lambda: web.open_new_tab('https://github.com/SoupCat-Py/NMStools/wiki'),
                                            fg_color=colors['main'], hover_color=colors['accent'], corner_radius=10)
        self.version =        ctk.CTkLabel(self, text='v0.1.0', font=(nms,15))

        # list of buttons for functions where all widgets are used
        self.sidebar_buttons = [self.solar_button, self.layline_button, self.glyph_button, self.log_button]

        # dict for functions where widget and name are used
        self.widgets = {
            self.solar_button   : 'solar',
            self.layline_button : 'layline',
            self.glyph_button   : 'glyph',
            self.log_button     : 'log'
        }
        
        # widget placement
        self.sidebar_title.grid( row=0,column=0, padx=15,pady=15, sticky='nsew')
        self.solar_button.grid(  row=1,column=0, padx=0, pady=10, sticky='w')
        self.layline_button.grid(row=2,column=0, padx=0, pady=10, sticky='w')
        self.glyph_button.grid(  row=3,column=0, padx=0, pady=10, sticky='w')
        self.log_button.grid(    row=4,column=0, padx=0, pady=10, sticky='w')
        self.settings_button.grid(row=5,column=0, padx=0,pady=20)
        self.help.place(         x = 75, y = 685)
        self.version.place(      x = 15, y = 685)

        # button bindings
        for widget in self.sidebar_buttons:                                          # for all widgets
            self.hover_bind(widget, self.widgets[widget])                            # hover/exit bind function
            widget.bind(left_click, lambda em, w=widget: self.click(w))              # bind left click


    # function to change images on hover/exit
    def hover_bind(self, widget, name):
        widget.bind('<Enter>', lambda e: None if tab == name else widget.configure(image=get_image(f'{name}_hov', 180,60)))
        widget.bind('<Leave>', lambda e: None if tab == name else widget.configure(image=get_image(f'{name}_norm', 180,60)))
        # check if tab is the same as widget
        # change if no

    # function for sidebar button click
    def click(self, target):
        for widget in self.sidebar_buttons:                                       
            mode = 'sel' if widget == target else 'norm'                                   # set mode for image - used to remove repitition
            widget.configure(image=get_image(f'{self.widgets[widget]}_{mode}', 180,60))    # change image
        self.master.switch_tab(self.widgets[target])
        self.sidebar_title.focus_set() if widget != target else None
        
    def open_settings(self):
        self.master.switch_tab('settings')
        for button in self.sidebar_buttons:                                            # reset all other buttons
            button.configure(image=get_image(f'{self.widgets[button]}_norm', 180,60))  # ^
        self.focus_set(self.sidebar_title) if tab != 'settings' else None              # remove focus from other tabs         

class main(ctk.CTk):
    # initalization
    def __init__(self):
        super().__init__()

        # main window config
        self.geometry('1080x720')
        self.resizable(False,False)
        if sys.platform == 'win32':
            import pywinstyles
            pywinstyles.apply_style(self, 'acrylic')
        self.title('')
        
        # background
        self.bg = ctk.CTkLabel(self, text='', image=get_image('bg',880,720))
        self.bg.place(x=200,y=0)

        # initialize sidebar
        self.sidebar = sidebarFrame(self)
        self.sidebar.grid(row=0,column=0, sticky='nsew')

        # initialize tabs
        self.solar_tab =    solarTab(   self)
        self.layline_tab =  laylineTab( self)
        self.glyph_tab =    glyphTab(   self)
        self.log_tab =      logTab(     self)
        self.settings_tab = settingsTab(self, self.glyph_tab)

        self.tab_dict = {
            'solar'   : self.solar_tab,
            'layline' : self.layline_tab,
            'glyph'   : self.glyph_tab,
            'log'     : self.log_tab,
            'settings': self.settings_tab
        }


    # tab switcher
    def switch_tab(self, tab_target):
        global tab

        # first update for debug & fast refresh
        self.update_idletasks()

        # check if user is clicking onto a DIFFERENT tab
        if tab != tab_target:
            for page in [self.solar_tab, self.layline_tab, self.glyph_tab, self.log_tab, self.settings_tab]: # remove all page frames
                page.grid_forget()                                                                           # ^
            dest_page = self.tab_dict[tab_target]          # get destination page from dict
            dest_page.grid(row=0,column=1, sticky='nsew')  # show the destination page
            tab = tab_target                               # set tab var
            self.update_idletasks()                        # update window for faster refresh

app = main()
app.mainloop()
save_settings()
os._exit(0)