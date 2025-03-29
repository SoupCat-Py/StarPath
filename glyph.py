# libraries used here
import customtkinter as ctk
import webbrowser as web

# other scripts
from var_handler import colors, nms, get_image
from layline import fade

class fromHex(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # SETUP
        self._corner_radius=20
        self.vc_h=self.register(self.validate_hex)

        # WIDGET INIT
        self.hex_input = ctk.CTkEntry(self, placeholder_text='input hex', font=(nms,30), width=220, height=50,
                                    validate='key', validatecommand=(self.vc_h,'%P', '%s','%S','%W'))
        self.clear_button = ctk.CTkButton(self, text='Clear', text_color=colors['main'], width=70, command=self.clear_all,
                                        fg_color='transparent', border_width=2, border_color=colors['main'], hover_color=colors['dark'])
        self.glyph_output_label = ctk.CTkLabel(self, text='Portal Address: ', font=(nms,20))
        
        # WIDGET PLACEMENT
        self.hex_input.grid         (row=0,column=0, padx=20,pady=20, sticky='e', columnspan=8)
        self.clear_button.grid      (row=0,column=8, padx=0, pady=20, sticky='w')
        self.glyph_output_label.grid(row=1,column=0, padx=15,pady=20)

        # special init and placement for glyphs
        self.glyph_output_dict = {}
        for i in range(12):
            output_name = f'glyph_output_{i}'
            self.glyph_output_dict[output_name] = ctk.CTkLabel(self, text='', image=get_image('portal-',40,40))
            self.glyph_output_dict[output_name].grid(row=1, column=i+1, padx=5,pady=5)

        self.hex_input.bind('<BackSpace>', self.check_for_last_deletion)

    
    def validate_hex(self, final, initial, new_char, entry):
        # allow blank or placeholder
        if final == '' or final == 'input hex':
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


            return True
        return False
    
    def check_for_last_deletion(self, unused_variable):
        if len(self.hex_input.get()) == 1:
                self.glyph_output_dict['glyph_output_0'].configure(image=get_image('portal-',40,40))

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

# class fromGlyph(ctk.CTkFrame):
# remember to add a backspace button and copy button

class glyphTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # WIDGET INIT
        self.from_hex_frame=fromHex(self)
        self.spacer = ctk.CTkLabel(self, text='', width=880)

        # WIDGET PLACEMENT
        self.spacer.grid(row=0,column=0)
        self.from_hex_frame.grid(row=1,column=0, padx=50, pady=50, sticky='nsew')