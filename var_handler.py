import customtkinter as ctk
from PIL import Image as image
from pathlib import Path
import os, sys, json, shutil



### variables used in other scripts ###

colors = {
    'main'   : '#d80000',   # main red
    'accent' : '#c20404',   # accent red - button norm
    'light'  : '#f82121',   # light red  - button hov
    'dark'   : '#9d0202',   # dark red   - button sel
    'blue-m' : '#036ffc',   # main blue  - copy button
    'blue-h' : '#083b80'    # hover blue - copy button
}

left_click = '<Button-1>' if sys.platform == 'darwin' else '<Button-0>'

tab = 'Main'
prefix = 'portal'





### images (i have no idea what's going on here) ###
    
# Find platform-appropriate App Support dir
if sys.platform == 'darwin':
    app_support_dir = Path.home() / 'Library/Application Support/StarPath'
elif sys.platform == 'win32':
    app_support_dir = Path(os.getenv('APPDATA')) / 'StarPath'
else:
    app_support_dir = Path.home() / '.starpath'

# make the Images directory
user_image_dir = app_support_dir / 'Images'
user_image_dir.mkdir(parents=True, exist_ok=True)

# check if user is in a bundled PyInstaller environment
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path  # bundled path
    return Path(relative_path)  # dev mode path

# Copy images only if not already copied
bundled_image_dir = resource_path('Images')
# Only copy images if the folder is empty
if not any(user_image_dir.iterdir()):
    for img in bundled_image_dir.iterdir():
        if img.suffix.lower() == ".png":
            shutil.copy(img, user_image_dir / img.name)

# set image files in one line
def get_image(name, w,h):
    path = user_image_dir / f'{name}.png'
    return ctk.CTkImage(dark_image=image.open(path), light_image=image.open(path), size=(w,h))





### JSON shit ###

# create the JSON file
app_support_dir.mkdir(parents=True, exist_ok=True)  # create the folder if it doesn't exist
settings_file = app_support_dir / 'settings.json'   # set json file path
settings_file.touch(exist_ok=True)                  # create the file
        
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
def save_log():
    pass
        
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