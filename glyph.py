# libraries used here
import customtkinter as ctk
import webbrowser as web
import pyperclip as ppc

# other scripts
from var_handler import colors, nms, get_image, left_click
from layline import fade

global output_list, input_index
output_list = []
input_index = 0

class fromHex(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # SETUP
        self._corner_radius=20
        self.vc_h=self.register(self.validate_hex)

        # WIDGET INIT
        self.hex_input = ctk.CTkEntry(self, placeholder_text='input hex', font=(nms,30), width=300, height=50, justify='center',
                                    validate='key', validatecommand=(self.vc_h,'%P', '%s','%S','%W'))
        self.clear_button = ctk.CTkButton(self, text='Clear', text_color=colors['main'], width=70, command=self.clear_all,
                                        fg_color='transparent', border_width=2, border_color=colors['main'], hover_color=colors['dark'])
        self.glyph_output_label = ctk.CTkLabel(self, text='Portal Address: ', font=(nms,20))
        
        # WIDGET PLACEMENT
        self.hex_input.grid         (row=0,column=0,  padx=20, pady=20, sticky='e', columnspan=9)
        self.clear_button.grid      (row=0,column=10, padx=0,  pady=20, sticky='w')
        self.glyph_output_label.grid(row=1,column=0,  padx=15, pady=20)

        # special init and placement for glyphs
        self.glyph_output_dict = {}
        for i in range(12):
            output_name = f'glyph_output_{i}'
            self.glyph_output_dict[output_name] = ctk.CTkLabel(self, text='', image=get_image('portal-',40,40))
            self.glyph_output_dict[output_name].grid(row=1, column=i+1, padx=5,pady=5)

    
    def validate_hex(self, final, initial, new_char, entry):
        global output_list

        # allow placeholder
        if final == 'input hex':
            return True
        
        # check for length
        if len(final) > 12:
            self.glow_red(entry)
            return False
        
        # check for hex
        if new_char in '1234567890abcdefABCDEF':
            # set lists
            initial_list = list(initial)
            final_list   = list(final)

            # append hyphens until both are the same length
            while len(final_list) < len(initial_list):
                longer_list = initial_list
                final_list.append('-')
            else:
                longer_list = final_list
                initial_list.append('-')

            # set all glyphs that were used 
            for i in range(len(longer_list)):
                self.glyph_output_dict[f'glyph_output_{i}'].configure(image=get_image(f'portal{final_list[i].lower()}',40,40))

            # set output list for copying
            output_var = final.lower()
            output_list = list(output_var)
            return True
        
        # check for deletion
        if final == '':
            # clear all glyphs
            for i in range(12):
                self.glyph_output_dict[f'glyph_output_{i}'].configure(image=get_image('portal-',40,40))
            # update list
            output_list = []
            return True
        
        # do not allow if none of these conditions are met
        return False

    def clear_all(self):
        for glyph in range(len(self.hex_input.get())):
            self.glyph_output_dict[f'glyph_output_{glyph}'].configure(image=get_image('portal-',40,40))
        self.hex_input.delete(0,ctk.END) if self.hex_input.get() != 'input hex' else None
    
    def fade_back(self, entry):
        if self.fade_stage < len(fade):
            entry.configure(border_color=fade[self.fade_stage])
            self.fade_stage += 1
            entry.after(50, lambda: self.fade_back(entry))
    
    def glow_red(self, input_entry):
        entry_name = self.nametowidget(input_entry)  # get name of focused entry - from string to widget
        parent_entry = entry_name.winfo_parent()     # get parent of the new widget - remove .!entry
        entry = self.nametowidget(parent_entry)      # get name of parent entry

        self.fade_stage = 0     # set starting point for fade_back
        self.fade_back(entry)   # start the fading loop

class glyph_input_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # frame setup
        self._corner_radius = 10
        self._border_color = '#696969'
        self._border_width = 2
        self.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1) # center columns and set equal width

        # empty dir for glyph inputs
        glyph_input_dict={}

        # glyph setup
        for i in range(16):
            widget_name = f'glyph_input_{f'{i:X}'}'
            # init
            glyph_input_dict[widget_name] = ctk.CTkLabel(self, text='', image=get_image(f'portal{f'{i:X}'}',50,50))
            # placement
            glyph_row = 0 if i < 8 else 1
            glyph_column = i if i < 8 else i-8 
            glyph_input_dict[widget_name].grid(row=glyph_row, column=glyph_column, padx=20,pady=20)
            # bindings - return hex value instead of index
            glyph_input_dict[widget_name].bind(left_click, lambda em, h=f'{i:X}': self.glyph_input_click(parent, h))

    def glyph_input_click(self, parent, glyph_input):
        if len(output_list) < 12:
            # update list
            output_list.append(glyph_input)
            # update label
            global input_index
            output_list_temp = list(parent.hex_output.cget('text'))       # make a list from the text
            output_list_temp[input_index] = glyph_input                   # replace last item in list
            input_index += 1                                              # increase index
            parent.hex_output.configure(text=(''.join(output_list_temp))) # convert list back to string and set label
        else:
            self.glow_red_frame()

    def fade_back_frame(self):
        if self.fade_index < len(fade):                           # check if fade is complete
            self.configure(border_color = fade[self.fade_index])  # set color
            self.fade_index += 1                                  # increase index - go to next color
            self.after(50, lambda: self.fade_back_frame())        # circular function - wait 50ms and call again

    def glow_red_frame(self):
        self.configure(border_color = fade[0])  # set starting color - red
        self.fade_index = 0                     # set starting point for fade_back
        self.fade_back_frame()                  # call fade_bacl

class fromGlyph(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # window init
        self._corner_radius=20
        self.grid_columnconfigure((0,1,2), weight=1) # center columns and set equal width

        # WIDGET INIT
        self.glyph_input =      glyph_input_frame(self)
        self.hex_output =       ctk.CTkLabel( self, text='_'*12, font=('courier',40), anchor='center')
        self.backspace_button = ctk.CTkLabel( self, text='', image=get_image('backspace',50,50))
        self.clear_button =     ctk.CTkButton(self, text='Clear', text_color=colors['main'], width=70, height=30, command=self.clear_all,
                                        fg_color='transparent', border_width=2, border_color=colors['main'], hover_color=colors['dark'])

        # WIDGET PLACEMENT
        self.glyph_input.grid(     row=0,column=0, padx=20,pady=20, sticky='nsew', columnspan=3)
        self.hex_output.grid(      row=1,column=1, padx=20,pady=20, sticky='ew')
        self.clear_button.grid(    row=1,column=0, padx=20,pady=20, sticky='e')
        self.backspace_button.grid(row=1,column=2, padx=20,pady=20, sticky='w')

        # BINDINGS
        self.backspace_button.bind(left_click, lambda em: self.backspace())


    def backspace(self):
        global output_list, input_index
        if len(output_list) > 0:
            # remove last item from list
            output_list.pop()
            # update label
            output_list_temp = list(self.hex_output.cget('text'))       # make list from label
            output_list_temp[input_index-1] = '_'                       # replace last item in list with '_'
            input_index -= 1                                            # decrease index
            self.hex_output.configure(text=(''.join(output_list_temp))) # convert list back to string and set label


    def clear_all(self):
        global output_list, input_index
        output_list = []  # reset output list
        self.hex_output.configure(text='_'*12)  # reset output label
        input_index = 0  # reset index

class glyphTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # WIDGET INIT
        self.from_hex_frame =fromHex(self)
        self.from_glyph_frame = fromGlyph(self)
        self.spacer = ctk.CTkLabel(self, text='', width=880)
        self.type_selector = ctk.CTkSegmentedButton(self, values=['Glyph -> Hex','Hex -> Glyph'], command=self.type_callback,
                                                    font=(nms, 25), fg_color=colors['main'], selected_color=colors['dark'], unselected_color=colors['accent'], unselected_hover_color=colors['light'], selected_hover_color=colors['dark'])
        self.copy_button = ctk.CTkButton(self, text='Copy NMScord Emojis', font=(nms,15), height=30, corner_radius=10, command=self.copy,
                                         fg_color='transparent', border_width=2, border_color=colors['blue-m'], hover_color=colors['blue-h'], text_color=colors['blue-m'])

        # WIDGET PLACEMENT
        self.spacer.grid(row=0,column=0)
        self.type_selector.grid   (row=1,column=0, pady=10)
        self.from_glyph_frame.grid(row=2,column=0, padx=30,pady=50, sticky='nsew')
        self.copy_button.grid     (row=3,column=0, padx=250,pady=20, sticky='ew', columnspan=13)

        # set default for segButton
        self.type_selector.set('Glyph -> Hex')

    
    def type_callback(self, value):
        if value == 'Glyph -> Hex':
            self.from_hex_frame.grid_forget()
            self.from_glyph_frame.grid(row=2,column=0, padx=30,pady=50, sticky='nsew')
        elif value == 'Hex -> Glyph':
            self.from_glyph_frame.grid_forget()
            self.from_hex_frame.grid(row=2,column=0, padx=30,pady=50, sticky='nsew')

    def copy(self):
        global output_list

        # new list with emoji names
        copy_list = []
        for glyph in output_list:
            copy_list.append(f':portal{glyph}:')

        # join and copy
        copy_string  = ''.join(copy_list)
        ppc.copy(copy_string)