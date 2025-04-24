import customtkinter as ctk
import webbrowser as web
import os, sys

from var_handler import *
from glyph import glyphTab

class glyphSettingsFrame(ctk.CTkFrame):
    def __init__(self, master, glyphTab_instance):
        super().__init__(master)
        
        # store instances for later use
        self.glyph_tab = glyphTab_instance
        
        # useful vars
        self.presets = {
            'none'            : '',
            'NMScord'         : 'portal',
            'Oskar1up'        : 'hex_',
            'NMS Russia'      : 'Portal',
            'GerMan\'s Sky'   : 'glyphe',
            'NMS Francophone' : '_',
            'IEA'             : 'glyph_',
            'NMH'             : 'Glyph_'
        }
        self.presets_note_text = '''choose one of these presets to format emojis for that server.
select "none" if you want to make your own'''
        
        # widget init
        self.title = ctk.CTkLabel(self, text='Glyph Converter', font=(nms,25), text_color=colors['light'])
        self.emoji_toggle = ctk.CTkSwitch(self, text='enable emoji copying', font=(nms,20), command=self.emoji_toggle_command)
        self.prefix_label = ctk.CTkLabel(self, text='emoji prefix', font=(nms,20))
        self.prefix_entry = ctk.CTkEntry(self, placeholder_text='ie: "portal" -> :portal0:', font=(nms,20), width=200)
        self.prefix_apply = ctk.CTkButton(self, text='apply', font=(nms,18), width=10, command=self.apply_prefix)
        self.presets_label = ctk.CTkLabel(self, text='server preset', font=(nms,20))
        self.presets_dropdown = ctk.CTkOptionMenu(self, values=list(self.presets.keys()), font=(nms,20), width=200, command=self.presets_dropdown_command)
        self.presets_note = ctk.CTkLabel(self, text=self.presets_note_text, text_color='#7B7B7B', font=(nms,15))
        self.uppercase_check = ctk.CTkCheckBox(self, text='uppercase hex values', onvalue=True, offvalue=False, command=self.uppercase_check_command)
        
        #widget placement
        self.title.grid(       row=0,column=0,columnspan=3, padx=10,pady=20, sticky='ew')
        self.emoji_toggle.grid(row=1,column=0,columnspan=3, padx=10,pady=10)
        
        # set defaults
        if settings_dict['EnableEmoji']:
            self.emoji_toggle.select()
        else:
            self.emoji_toggle.deselect()
        #
        if settings_dict['EmojiUppercase']:
            self.uppercase_check.select()
        else:
            self.uppercase_check.deselect()
        #
        self.presets_dropdown.set(settings_dict['EmojiPreset'])
        if settings_dict['EmojiPreset'] != 'none':
            self.prefix_entry.insert(0,settings_dict['EmojiPrefix'])
        # run commands on init
        self.emoji_toggle_command()
        self.presets_dropdown_command(settings_dict['EmojiPreset'])
        
    def emoji_toggle_command(self):
        settings_dict["EnableEmoji"] = True if self.emoji_toggle.get() == 1 else False    
        self.glyph_tab.toggle_copy_button(self.emoji_toggle.get())
        
    def presets_dropdown_command(self, choice):
        global settings_dict
        settings_dict["EmojiPrefix"] = self.presets[choice]
        settings_dict["EmojiPreset"] = choice
        
        if choice == 'none':
            pass
            self.prefix_label.grid(    row=2,column=0,              padx=10,pady=10, sticky='e')
            self.prefix_entry.grid(    row=2,column=1,              padx=10,pady=10, sticky='ew')
            self.prefix_apply.grid(    row=2,column=2,              padx=10,pady=10, sticky='w')
            self.uppercase_check.grid( row=3,column=1,columnspan=2, padx=10,pady=10, sticky='ew')
            self.presets_label.grid(   row=4,column=0,              padx=10,pady=10, sticky='e')
            self.presets_dropdown.grid(row=4,column=1,columnspan=2, padx=10,pady=10, sticky='ew')
            self.presets_note.grid(    row=5,column=0,columnspan=3, padx=10,pady=10, sticky='ew')
            self.glyph_tab.copy_button.configure(text='Copy Emojis')
        else:
            self.prefix_label.grid_forget()
            self.prefix_entry.grid_forget()
            self.uppercase_check.grid_forget()
            self.presets_label.grid(   row=2,column=0,              padx=10,pady=10, sticky='e')
            self.presets_dropdown.grid(row=2,column=1,columnspan=2, padx=10,pady=10, sticky='ew')
            self.presets_note.grid(    row=3,column=0,columnspan=3, padx=10,pady=10)
            self.glyph_tab.copy_button.configure(text=f'Copy Emojis ({choice})')
            
    def uppercase_check_command(self):
        settings_dict['EmojiUppercase'] = self.uppercase_check.get()
        
    def apply_prefix(self):
        settings_dict['EmojiPrefix'] = self.prefix_entry.get()
        

class settingsTab(ctk.CTkFrame):
    def __init__(self, master, glyphTab_instance):
        super().__init__(master)
    
        # frame config
        self.grid_columnconfigure([0,1], weight=1)
        self.grid_rowconfigure([2,3,4], weight=1)
        
                
        # WIDGET CONFIG
        self.spacer = ctk.CTkLabel(self, text='', width=880, height=1)
        self.settings_title = ctk.CTkLabel(self, text='StarPath Settings', font=(nms,40), text_color=colors['light'])
        self.dev_button = ctk.CTkButton(self, text='Developer Mode', font=(nms, 20), command=self.secret,
                                           fg_color=colors['accent'], hover_color=colors['dark'], width=200, height=30)
        self.issues_button = ctk.CTkLabel(self, text='', image=get_image('github_closed',50,50))
        self.email_button  = ctk.CTkLabel(self, text='', image=get_image('mail_closed',50,50))
        #
        glyph_settings = glyphSettingsFrame(self, glyphTab_instance)
        
        # WIDGET PLACEMENT
        self.spacer.grid(        row=0,column=0, columnspan=2, sticky='ew')
        self.settings_title.grid(row=1,column=0, columnspan=2, padx=20,pady=20, sticky='nsew')
        self.dev_button.grid(    row=5,column=0, columnspan=2, padx=20,pady=20)
        self.issues_button.place(x=810,y=650)
        self.email_button.place( x=810,y=580)
        #
        glyph_settings.grid(     row=2,column=0, padx=20,pady=20, sticky='nw')
        
        # contact button bindings
        self.email_button.bind('<Enter>',  lambda e: self.expand_button(self.email_button))
        self.email_button.bind('<Leave>',  lambda e: self.collapse_button(self.email_button))
        self.email_button.bind(left_click, lambda e: web.open_new_tab('https://mail.google.com/mail/?view=cm&fs=1&to=soupcat.py@gmail.com'))
        self.issues_button.bind('<Enter>',  lambda e: self.expand_button(self.issues_button))
        self.issues_button.bind('<Leave>',  lambda e: self.collapse_button(self.issues_button))
        self.issues_button.bind(left_click, lambda e: web.open_new_tab('https://github.com/SoupCat-Py/StarPath/issues/new'))
        
        # TODO:
        # import/export log file for coordinate log
        # reset log
        # themes
        # change font?
        # app icon?
        
    def expand_button(self, button):
        if int(button.winfo_x()) > 800:
            if button == self.issues_button:
                button.configure(image=get_image('github_open',250,50))
                button.place(x=610,y=650)
            elif button == self.email_button:
                button.configure(image=get_image('mail_open',235,50))
                button.place(x=625,y=580)
            
    def collapse_button(self, button):
        if button == self.issues_button:
            button.configure(image=get_image('github_closed',50,50))
            button.place(x=810,y=650)
        elif button == self.email_button:
            button.configure(image=get_image('mail_closed',50,50))
            button.place(x=810,y=580)

    def secret(self):
        video_path = os.path.expanduser('~/Desktop/git/StarPath/Images/video.mp4')
        if sys.platform == 'darwin':
            import subprocess
            subprocess.run(['open', video_path])
        elif sys.platform == 'win32':
            os.startfile(video_path)
            # import pyautogui
            # self.after(2000, lambda: pyautogui.press('space'))