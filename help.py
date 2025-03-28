import customtkinter as ctk
import os
from var_handler import tab as set_tab
from var_handler import colors

is_open = False

class tabGroup(ctk.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # setup
        self.width=453
        self.height=450
        self.configure(segmented_button_fg_color = colors['main'],
                       segmented_button_unselected_color = colors['accent'],
                       segmented_button_selected_color = colors['dark'],
                       segmented_button_unselected_hover_color = colors['light'],
                       segmented_button_selected_hover_color = colors['dark'],
                       border_width=3,
                       border_color=colors['main'])

        # add/set tabs
        tab_list = ['Main','Solar','Layline','Glyph','Log']
        for tab in tab_list:
            self.add(tab)
        self.set(set_tab)

        self.destroy_button = ctk.CTkButton(master=self.tab('Main'), text='destroy', command=destroy_help_window)
        self.destroy_button.grid(row=0,column=0, padx=10,pady=10)

class helpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # tell the script the window is open
        global is_open
        is_open = True

        # window setup
        self.attributes('-topmost', True) # keep on top
        self.geometry('500x500')

        # widget init
        self.tabs = tabGroup(self, width=460, height=460)

        # widget placement
        self.tabs.place(relx=0.5,rely=0.5, anchor='center')

def open_help_window(parent):
    # check if the window is already open
    # if not, open the window and set false when closed
    global is_open, window
    if not is_open:
        window = helpWindow(parent)

def destroy_help_window():
    global is_open, window
    if window is not None:
        window.destroy()
        is_open = False