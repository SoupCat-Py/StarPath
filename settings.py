import customtkinter as ctk
import webbrowser as web
import matplotlib.font_manager as font_manager
import os, sys, subprocess

from var_handler import *

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
        self.emoji_toggle = ctk.CTkSwitch(self, text='enable emoji copying', font=('Verdana',15), command=self.emoji_toggle_command, progress_color=colors['main'])
        self.prefix_label = ctk.CTkLabel(self, text='emoji prefix', font=('Verdana',15))
        self.prefix_entry = ctk.CTkEntry(self, placeholder_text='ie: "portal" -> :portal0:', font=('Verdana',15), width=200)
        self.prefix_apply = ctk.CTkButton(self, text='APPLY', font=('Verdana',12), width=10, command=self.apply_prefix, fg_color=colors['main'], hover_color=colors['dark'])
        self.presets_label = ctk.CTkLabel(self, text='server preset', font=('Verdana',15))
        self.presets_dropdown = ctk.CTkOptionMenu(self, values=list(self.presets.keys()), font=('Verdana',15), width=200, command=self.presets_dropdown_command,
                                                  fg_color=colors['main'], button_color=colors['dark'], button_hover_color=colors['light'])
        self.presets_note = ctk.CTkLabel(self, text=self.presets_note_text, text_color='#7B7B7B', font=('Verdana',15))
        self.uppercase_check = ctk.CTkCheckBox(self, text='uppercase hex values', font=('Verdana',15), onvalue=True, offvalue=False, command=self.uppercase_check_command, 
                                               fg_color=colors['main'], hover_color=colors['dark'])
        
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
        save_settings()
        
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
        save_settings()
            
    def uppercase_check_command(self):
        settings_dict['EmojiUppercase'] = self.uppercase_check.get()
        save_settings()
        
    def apply_prefix(self):
        settings_dict['EmojiPrefix'] = self.prefix_entry.get()
        save_settings()   
        
class generalSettingsFrame(ctk.CTkFrame):
    def __init__(self, master, main_instance) :
        super().__init__(master)
        
        self.grid_rowconfigure([0,1,2,3], weight=1)
        self.grid_columnconfigure([0,1,2], weight=1)
        
        # pass main window instance
        self.main_instance = main_instance
        
        # accepted fonts
        fonts=['GeosansLight-NMS','Futura','Arial','Verdana','Tahoma','Trebuchet MS','Times New Roman','Georgia','Courier New','Roboto','Garamond','Montsterrat',
               'Product Sans','Open Sans', 'DESIGNER','Entirely','Black Future','Project Sans','Nunito','Calibri','Comic Sans MS','DIN Alternate','Euphemia UCAS']
        for font in fonts:
            if font not in font_manager.get_font_names():
                fonts.remove(font)
                
        # WIDGET INIT
        self.title = ctk.CTkLabel(self, text='General', font=(nms,25), text_color=colors['light'])
        self.font_label = ctk.CTkLabel(self, text='''Custom font: \n (requires restart)''', font=('Verdana',15))
        self.font_picker = ctk.CTkOptionMenu(self, values=sorted(fonts), width=250, font=(nms,20), command=self.set_font,
                                             fg_color=colors['main'], button_color=colors['dark'], button_hover_color=colors['light'])
        self.nms_font_button = ctk.CTkButton(self, text='get the No Man\'s Sky font', command=lambda: web.open_new_tab('https://fontmeme.com/fonts/geo-nms-font/'),
                                             fg_color=colors['main'],hover_color=colors['dark'])
        self.restart_button = ctk.CTkButton(self, text='restart StarPath', font=('Verdana',15), command=self.restart,
                                            fg_color='transparent', hover_color=colors['dark'], border_color=colors['main'], text_color=colors['main'], border_width=2, corner_radius=20)
        
        # WIDGET PLACEMENT
        self.title.grid(          row=0,column=0,columnspan=3, padx=10,pady=20)
        self.font_label.grid(     row=1,column=0,              padx=10,pady=10, sticky='se')
        self.font_picker.grid(    row=1,column=1,              padx=10,pady=10, sticky='ew')
        self.nms_font_button.grid(row=3,column=0,columnspan=2, padx=10,pady=10, sticky='ew')
        self.restart_button.grid( row=1,column=2,rowspan=3,    padx=10,pady=20, sticky='nsw')
        
        # set defaults
        self.font_picker.set(settings_dict['Font'])
        
    def set_font(self, choice):
        settings_dict['Font'] = choice                # update the dict
        self.font_picker.configure(font=(choice,20))  # update the widget so the user can have a preview
        self.restart_button.configure(fg_color='#751717')
        save_settings()
        
    def restart(self):
        save_settings()

        if getattr(sys, 'frozen', False):
            # App is bundled (frozen = PyInstaller or similar)
            if sys.platform == 'darwin':
                # macOS: open the .app bundle using `open`
                app_path = os.path.abspath(sys.argv[0])
                if app_path.endswith("/Contents/MacOS/" + os.path.basename(app_path)):
                    app_path = app_path.split("/Contents/")[0] + ".app"
                subprocess.Popen(["open", app_path])
            elif sys.platform == 'win32':
                # Windows: re-launch the .exe directly
                subprocess.Popen([sys.executable])
        else:
            # Dev mode (running .py file): use execv
            os.execv(sys.executable, [sys.executable] + sys.argv)

        sys.exit()  # ensure current process exits
            
class settingsTab(ctk.CTkFrame):
    def __init__(self, master, glyphTab_instance, main_instance):
        super().__init__(master)
    
        # frame config
        self.grid_rowconfigure([2,3,4], weight=1)
        
                
        # WIDGET CONFIG
        self.spacer = ctk.CTkLabel(self, text='', width=880, height=1)
        self.settings_title = ctk.CTkLabel(self, text='StarPath Settings', font=(nms,40), text_color=colors['light'])
        self.dev_button = ctk.CTkButton(self, text='Developer Mode', font=(nms, 20), command=self.secret,
                                           fg_color=colors['accent'], hover_color=colors['dark'], width=200, height=30)
        #
        general_settings = generalSettingsFrame(self, main_instance)
        glyph_settings = glyphSettingsFrame(self, glyphTab_instance)
        
        # WIDGET PLACEMENT
        self.spacer.grid(        row=0,column=0, sticky='ew')
        self.settings_title.grid(row=1,column=0, padx=20,pady=20, sticky='nsew')
        self.dev_button.grid(    row=4,column=0, padx=20,pady=00, sticky='n')
        #
        general_settings.grid(   row=2,column=0, padx=20,pady=10, sticky='nsew')
        glyph_settings.grid(     row=3,column=0, padx=20,pady=10, sticky='nsew')

    def secret(self):
        video_path = os.path.expanduser('~/Desktop/git/StarPath/Images/video.mp4')
        if sys.platform == 'darwin':
            import subprocess
            subprocess.run(['open', video_path])
        elif sys.platform == 'win32':
            os.startfile(video_path)
            # import pyautogui
            # self.after(2000, lambda: pyautogui.press('space'))