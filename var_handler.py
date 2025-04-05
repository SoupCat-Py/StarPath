import customtkinter as ctk
from PIL import Image as image
import os, sys

colors = {
    'main'   : '#d80000',   # main red
    'accent' : '#c20404',   # accent red - button norm
    'light'  : '#f82121',   # light red - button hov
    'dark'   : '#9d0202',   # dark red - button sel
    'blue-m' : '#036ffc',   # main blue - copy button
    'blue-h' : '#083b80'    # hover blue - copy button
}

# left click for macOS and Windows
left_click = '<Button-1>' if sys.platform == 'darwin' else '<Button-0>'

nms = 'GeosansLight-NMS'
tab = 'Main'

# set image files in one line
os.chdir(os.path.expanduser('~/Desktop/git/StarPath'))
def get_image(name, w,h):
    # add try/except to see if the file exists first
    return ctk.CTkImage(dark_image=image.open(f'Images/{name}.png'), light_image=image.open(f'Images/{name}.png'), size=(w,h))


# store other variables here such as logged coords