import customtkinter as ctk
from PIL import Image as image
from pathlib import Path
from contextlib import suppress
import os, sys, json

colors = {
    'main'   : '#d80000',   # main red
    'accent' : '#c20404',   # accent red - button norm
    'light'  : '#f82121',   # light red  - button hov
    'dark'   : '#9d0202',   # dark red   - button sel
    'blue-m' : '#036ffc',   # main blue  - copy button
    'blue-h' : '#083b80'    # hover blue - copy button
}

# left click for macOS and Windows
left_click = '<Button-1>' if sys.platform == 'darwin' else '<Button-0>'

tab = 'Main'
prefix = 'portal'

# set image files in one line
os.chdir(os.path.expanduser('~/Desktop/git/StarPath')) # change this later when program is done / in dist phase
def get_image(name, w,h):
    # add try/except to see if the file exists first
    return ctk.CTkImage(dark_image=image.open(f'Images/{name}.png'), light_image=image.open(f'Images/{name}.png'), size=(w,h))

# default file for JSON logging
if sys.platform == 'darwin':
    app_support_dir = Path.home() / 'Library' / 'Application Support' / 'StarPath'  # get the folder to log stuff (and add images)
    
app_support_dir.mkdir(parents=True, exist_ok=True)                                  # create the folder if it doesn't exist
log_file = app_support_dir / 'log.json'                                             # set json file path
settings_file = app_support_dir / 'settings.json'
log_file.touch(exist_ok=True)       # create the files
settings_file.touch(exist_ok=True)  # ^
        
# read settings file
settings_dict = {}
with open(settings_file, 'r') as settings:
    try:
        settings_dict = json.load(settings)
    except:
        settings_dict = {}

# writing to JSON
def save_settings():
    with open(settings_file, 'w') as settings:
        json.dump(settings_dict, settings, indent=1)
        
# set default settings
def default(key, value):
    global settings_dict
    if key not in settings_dict:
        settings_dict[key] = value
default('EnableEmoji', True)
default('EmojiPrefix', 'portal')
default('EmojiPreset', 'NMScord')
default('EmojiUppercase', True)
default('Font', 'GeosansLight-NMS')
save_settings()
    
nms = settings_dict['Font']
        
# copy all the other files over - images