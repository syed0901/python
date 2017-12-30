import re
import os
import time
import json
import requests
import urllib2
import shutil
import commands
import ctypes
import struct
from wsgiref import headers
from notif import *

#time.sleep(5)

def change_wallpaper():
    sys_parameters_info = get_sys_parameters_info()
    rs = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, WALLPAPER_PATH, 3)

    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not rs:
        print(ctypes.WinError())


def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA

URL = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"

image_data = json.loads(requests.get(URL).text)
image_url = 'http://www.bing.com' + image_data['images'][0]['url']

##########################################################################################
# url for better quality image
image_download_url = 'http://www.bing.com/hpwp/' + image_data['images'][0]['hsh']
image_name = image_url[re.search("rb/", image_url).end():re.search('_EN', image_url).start()] + '.jpg'
##########################################################################################
w=WindowsBalloonTip()
file_path = 'C:\\Pictures\\Bing_Pic_of_the_Day\\' + image_name

if os.path.exists(file_path) is False:
    # try downloading by second url
    r=requests.get(image_download_url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(r.raw, out_file)
        w.handleNotif("Wallpaper successfully changed with Bing", file_path)
        del r
    else:
        r=requests.get(image_url, stream=True)
        if r.status_code == 200:
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            w.handleNotif("Wallpaper successfully changed with Bing", file_path)
            del r
        else:
            w.handleNotif("ERROR","Wallpaper not downloaded")
else:
    w.handleNotif("Wallpaper already downloaded", file_path)
    #print 'Wallpaper already downloaded. '+file_path 

SPI_SETDESKWALLPAPER = 20
WALLPAPER_PATH = file_path
change_wallpaper()