import customtkinter as ctk
import webbrowser as web
from var_handler import *

class helpTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # widget init
        self.spacer = ctk.CTkLabel(self, text='', width=880)
        self.title = ctk.CTkLabel(self, text='StarPath Help', font=(nms, 30), text_color=colors['main'])
        #
        self.logo = ctk.CTkLabel(self, text='', image=get_image('mac',300,300))
        self.version = ctk.CTkLabel(self, text='version 0.1.0\n(in development)', font=('Courier',25))
        self.spacer2 = ctk.CTkLabel(self, text=('-'*100), width=880, height=50)
        #
        self.wiki_button = ctk.CTkLabel(self, text='', image=get_image('wiki_closed', 200,200))
        self.issues_button = ctk.CTkButton(self, text='Submit GitHub Issue', command=lambda: web.open_new_tab('https://github.com/SoupCat-Py/StarPath/issues/new'),
                                           image=get_image('issue_icon',50,50), corner_radius=60, font=('Verdana', 15), fg_color=colors['accent'], hover_color=colors['dark'])
        self.email_button  = ctk.CTkButton(self, text='Contact Soup', command=lambda: web.open_new_tab('https://mail.google.com/mail/?view=cm&fs=1&to=soupcat.py@gmail.com'),
                                           image=get_image('email_icon',50,50), corner_radius=60, font=('Verdana', 15), fg_color=colors['accent'], hover_color=colors['dark'])
        
        # widget placement
        self.spacer.grid(       row=0,column=0, sticky='ew', columnspan=2) ##
        self.title.grid(        row=1,column=0, sticky='ew', columnspan=2)
        #
        self.logo.grid(         row=2,column=0, sticky='ew', columnspan=2)
        self.version.grid(      row=3,column=0, sticky='ew', columnspan=2)
        self.spacer2.grid(      row=4,column=0, sticky='ew', columnspan=2) ##
        #
        self.wiki_button.grid(  row=5,column=0, sticky='e',  rowspan=2, padx=50)
        self.issues_button.grid(row=5,column=1, sticky='w')
        self.email_button.grid( row=6,column=1, sticky='w')
        
        self.wiki_button.bind('<Enter>', lambda e: self.wiki_button.configure(image=get_image('wiki_open', 200,200)))
        self.wiki_button.bind('<Leave>', lambda e: self.wiki_button.configure(image=get_image('wiki_closed', 200,200)))
        self.wiki_button.bind(left_click, lambda e: web.open_new_tab('https://github.com/SoupCat-Py/StarPath/wiki'))