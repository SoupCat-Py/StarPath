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
        self.hex_input=ctk.CTkEntry(self, placeholder_text='input hex', font=(nms,30), width=220, height=50,
                                    validate='key', validatecommand=(self.vc_h,'%P','%W'))
        self.glyph_output_label = ctk.CTkLabel(self, text='Portal Address: ', font=(nms,20))
        
        # WIDGET PLACEMENT
        self.hex_input.grid(row=0,column=0, padx=20,pady=20, columnspan=13)
        self.glyph_output_label.grid(row=1,column=0, padx=15,pady=20)

        # special init and placement for glyphs
        self.glyph_output_dict = {}
        for i in range(12):
            output_name = f'glyph_output_{i}'
            self.glyph_output_dict[output_name] = ctk.CTkLabel(self, text='', image=get_image('portalnone',40,40))
            self.glyph_output_dict[output_name].grid(row=1, column=i+1, padx=5,pady=5)


    def validate_hex(self, input, entry):
        # check for blank or placeholder
        if input == 'input hex' or input == '':
            return True
        # check for hex
        elif input[len(input)-1] in '1234567890ABCDEFabcdef':
            # check for length
            if len(input) > 12:   # show user if limit is reached
                self.glow_red(entry)
                return False
            else:   # update
                if len(input) > 0:
                    glyph = (input[-1:]).lower()    # get the lowercase last character
                    target_image = f'portal{glyph}' # get the image needed
                    target_widget_name = f'glyph_output_{len(input)-1}'          # get the name of target widget
                    target_widget = self.glyph_output_dict[target_widget_name]   # get target widget itself
                    target_widget.configure(text='', image=get_image(target_image,40,40)) # change image
                return True
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

# class fromGlyph(ctk.CTkFrame):

class glyphTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # WIDGET INIT
        self.from_hex_frame=fromHex(self)
        self.spacer = ctk.CTkLabel(self, text='', width=880)

        # WIDGET PLACEMENT
        self.spacer.grid(row=0,column=0)
        self.from_hex_frame.grid(row=1,column=0, padx=50, pady=50, sticky='nsew')