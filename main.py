from pymem import *
from pymem.process import *
import PySimpleGUI as sg
from ReadWriteMemory import ReadWriteMemory
import win32process
import win32api
import psutil
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound

#variables
address = 0
coins_point=0
base_address=0
language = "ru"
dmg =0
red_heart=0
coins = 0
bombs = 0
keys = 0
win_close=0
process_hook_status=0
charges=0
blue_heart=0
process_hook_stop=0
###############################################################################

###############################################################################

#window config
sg.theme('DarkAmber')
def layout(language):
    if language == "ru":
        main_window_layout = [  [sg.Text("Только целые числа",s=49),sg.Button("Hook",key="new_run",s=6),sg.Button("RU/EN",key = "Change_language",s=5)],
        [sg.Text('Монеты',s=8), sg.InputText(),sg.Button("Изменить",key="Change_coins"),sg.Button("∞ 99",key="inf_coins",s=4)],
        [sg.Text('Бомбы',s=8), sg.InputText(),sg.Button("Изменить",key="Change_bombs"),sg.Button("∞ 99",key="inf_bombs",s=4)],
        [sg.Text('Ключи',s=8), sg.InputText(),sg.Button("Изменить",key="Change_keys"),sg.Button("∞ 99",key="inf_keys",s=4)],
        [sg.Text("ID Активки",s=8),sg.InputText(),sg.Button("Изменить",key="Change_active_item"),sg.Button("D6",key="give_d6",s=4)],
        [sg.Frame("",[[sg.Text("Left ctrl + 1 - Бесконечные монеты",s=28),sg.Text("Left ctrl + 5 - Бесконечные красные сердца",s=33)],
        [sg.Text("Left ctrl + 2 - Бесконечные бомбы",s=28),sg.Text("Left ctrl + 6 - Бесконечные синие сердца",s=33)],
        [sg.Text("Left ctrl + 3 - Бесконечные ключи",s=28),sg.Text("Left ctrl + 7 - Бесконечные заряды активки",s=33)],
        [sg.Text("Left ctrl + 4 - 100 Урона")]])],
        [sg.Button("Бесконечный заряд активного предмета",key="inf_charges"),sg.Button("100 Урона",key="100 Damage",s=13)],
        [sg.Button("Бесконечные красные сердца",key="inf_red_heart"),sg.Button("Бесконечные синие сердца",key="inf_blue_heart",s=21)],
        [sg.Text("")],
        [sg.Button('Выход',key="Exit"),sg.Text("",s=35),sg.Text("Made by GAVKOSHMIG Inc.")]]
    else:
        main_window_layout = [  [sg.Text("Only integer numbers",s=49),sg.Button("Hook",key="new_run",s=6),sg.Button("RU/EN",key = "Change_language",s=5)],
        [sg.Text('Coins',s=8), sg.InputText(),sg.Button("Change",key="Change_coins"),sg.Button("Inf 99",key="inf_coins",s=4)],
        [sg.Text('Bombs',s=8), sg.InputText(),sg.Button("Change",key="Change_bombs"),sg.Button("Inf 99",key="inf_bombs",s=4)],
        [sg.Text('Keys',s=8), sg.InputText(),sg.Button("Change",key="Change_keys"),sg.Button("Inf 99",key="inf_keys",s=4)],
        [sg.Text("Active item ID",s=10),sg.InputText(s=43),sg.Button("Change",key="Change_active_item"),sg.Button("D6",key="give_d6",s=4)],
        [sg.Frame("",[[sg.Text("Left ctrl + 1 - Inf coins",s=28),sg.Text("Left ctrl + 5 - Inf red hearts",s=33)],
        [sg.Text("Left ctrl + 2 - Inf bombs",s=28),sg.Text("Left ctrl + 6 - Inf blue hearts",s=33)],
        [sg.Text("Left ctrl + 3 - Inf keys",s=28),sg.Text("Left ctrl + 7 - Inf active item",s=33)],
        [sg.Text("Left ctrl + 4 - 100 Damage")]])],
        [sg.Button("Inf active item charge",key="inf_charges"),sg.Button("100 Damage",key="100 Damage",s=13)],
        [sg.Button("Inf red hearts",key="inf_red_heart"),sg.Button("Inf blue hearts",key="inf_blue_heart",s=19)],
        [sg.Text("")],
        [sg.Button('Exit',key="Exit"),sg.Text("",s=35),sg.Text("Made by GAVKOSHMIG Inc.")]]
    return sg.Window("Isaac's cheats",main_window_layout)
###############################################################################

#error window cfg
error_window_layout = [[sg.Text("Your input not integer number!")],
           [sg.Button("Close",key="Close_error")]]
error_window = sg.Window("Error",error_window_layout)
###############################################################################

#write funcs
def coins_write(coins_count):
    process.write(coins_point,coins_count)
def bombs_write(bombs_count):
    process.write(bombs_point,bombs_count)
def keys_write(keys_count):
    process.write(keys_point,keys_count)
def damage_write():
    process.write(damage_point,1120403000)
def red_heart_write():
    process.write(red_heart_point, 24)
def charges_write():
    process.write(charges_point, 6)
def active_item_write(item_id):
    process.write(active_item_point,item_id)
def blue_heart_write():
    process.write(blue_heart_point, 8)



###############################################################################

#error window
def write_and_error_window(value,thing):
    try:
        value = int(value)
        if thing == "coins":
            coins_write(int(value))
        elif thing == "bombs":
            bombs_write(int(value))
        elif thing == "keys":
            keys_write(int(value))
        elif thing == "active_item":
            active_item_write(int(value))
    except:
        if language == "ru":
            winsound.PlaySound("ButtonClick.wav", 1)
            sg.popup("Вы ввели не целое число!",title="ERROR!")
        else:
            winsound.PlaySound("ButtonClick.wav", 1)
            sg.popup("Your input isn't integer number!",title="ERROR!")
###############################################################################

#loop new
def inf_coins():
    global coins
    if coins == 0:
        coins = 1
        def everlasting_coins():
            global coins
            while coins == 1:
                    coins_write(99)
                    sleep(1)
        Thread(target=everlasting_coins).start()
    elif coins == 1:
        coins = 0

def inf_bombs():
    global bombs
    if bombs == 0:
        bombs = 1
        def everlasting_bombs():
            global bombs
            while bombs == 1:
                bombs_write(99)
                sleep(1)
        Thread(target=everlasting_bombs).start()
    elif bombs == 1:
        bombs = 0

def inf_keys():
    global keys
    if keys == 0:
        keys = 1
        def everlasting_keys():
            global keys
            while keys == 1:
                keys_write(99)
                sleep(1)
        Thread(target=everlasting_keys).start()
    elif keys == 1:
        keys = 0

def inf_red_heart():
    global red_heart
    if red_heart == 0:
        red_heart = 1
        def everlasting_red_heart():
            global red_heart
            while red_heart == 1:
                red_heart_write()
                sleep(1)
        Thread(target=everlasting_red_heart).start()
    elif red_heart == 1:
        red_heart = 0

def inf_charges():
    global charges
    if charges == 0:
        charges = 1
        def everlasting_charges():
            global charges
            while charges == 1:
                charges_write()
                sleep(0.2)
        Thread(target=everlasting_charges).start()
    elif charges == 1:
        charges = 0

def inf_100_dmg():
    global dmg
    if dmg == 0:
        dmg = 1
        def everlasting_dmg():
            global dmg
            while dmg == 1:
                damage_write()
                sleep(1)
        Thread(target=everlasting_dmg).start()
    elif dmg == 1:
        dmg = 0

def inf_blue_heart():
    global blue_heart
    if blue_heart == 0:
        blue_heart = 1
        def everlasting_blue_heart():
            global blue_heart
            while blue_heart == 1:
                blue_heart_write()
                sleep(1)
        Thread(target=everlasting_blue_heart).start()
    elif blue_heart == 1:
        blue_heart = 0

###############################################################################

#window logic
window = (layout(language))
def main():
    global coins_point,bombs_point,keys_point,damage_point,address,process,process_hook_status,red_heart_point,charges_point,active_item_point,blue_heart_point,win_close
    global process,base_address
    global coins, bombs,keys,win_close,process_hook_status,language,window
    event, values = window.read(timeout=10)
    print(event)
    #loop things
    if event =="inf_coins":
        inf_coins()
    if event == "inf_bombs":
        inf_bombs()
    if event == "inf_keys":
        inf_keys()
    if event == "inf_red_heart":
        inf_red_heart()
    if event == "inf_charges":
        inf_charges()
    if event == "100 Damage":
        inf_100_dmg()
    if event == "inf_blue_heart":
        inf_blue_heart()


    #writtable things
    if event == "Change_coins":
        write_and_error_window(values[0],"coins")
    if event == "Change_bombs":
        write_and_error_window(values[1],"bombs")
    if event == "Change_keys":
        write_and_error_window(values[2],"keys")
    if event == "Change_active_item":
        write_and_error_window(values[3],"active_item")
    
    #misc
    if event == "new_run":
        try:
            inf_hook()
        except: pass
    if event == "give_d6":
        write_and_error_window(105,"active_item")
    if event == "Change_language":
        window.close()
        if language == "ru":
            language = "en"
            window = (layout(language))
        else:
            language = "ru"
            window = (layout(language))
    #exit
    if event == sg.WIN_CLOSED or event == 'Exit':
        win_close=1
        window.close()    
###############################################################################

#hotkeys
def hotkeys():
    global hotkey
    with keyboard.GlobalHotKeys({
        "<ctrl>+1":inf_coins,
        "<ctrl>+2":inf_bombs,
        "<ctrl>+3":inf_keys,
        "<ctrl>+4":inf_100_dmg,
        "<ctrl>+5":inf_red_heart,
        "<ctrl>+6":inf_blue_heart,
        "<ctrl>+7":inf_charges}) as hotkey:
        hotkey.join()
Thread(target=hotkeys).start()
###############################################################################



###############################################################################




#process hook and pointers
def inf_hook():
    global coins_point,bombs_point,keys_point,damage_point,address,process,process_hook_status,red_heart_point,charges_point,active_item_point,blue_heart_point,win_close
    global charges,red_heart,blue_heart,coins,bombs,keys,base_address
    my_pid = None
    pids = None
    ps = None
    pids = psutil.pids()
    for pid in pids:
        ps = psutil.Process(pid) 
        if "isaac-ng.exe" in ps.name():
            my_pid = ps.pid
    PROCESS_ALL_ACCESS = 0x1F0FFF
    processHandle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, my_pid)
    modules = win32process.EnumProcessModules(processHandle)
    processHandle.close()
    base_address = modules[0]
    print(base_address)
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name("isaac-ng.exe")
    process.open()
    pm = Pymem("isaac-ng.exe")
    base_address = pm.base_address
    address = base_address+0x804270


    coins_point = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x358,0x0,0x12B8])
    process_hook_status = 1
    bombs_point = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x12B4])
    keys_point = process.get_pointer(address, offsets=[0x4,0x1C,0xBBC,0x16C,0x0,0x12AC])
    damage_point = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x13B8])
    red_heart_point = process.get_pointer(address,offsets=[0x4,0x1C,0x9F0,0x23C,0x16C,0x0,0x1294])
    charges_point = process.get_pointer(address,offsets=[0x4,0x0,0x4,0x1C,0xCF8,0x0,0x14C8])
    active_item_point = process.get_pointer(address,offsets=[0x8,0x1C,0x9F0,0x30,0x358,0x0,0x14C4])
    blue_heart_point = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x50,0x358,0x0,0x129C])


    if coins_point == 4792:
        if language == "ru":
            winsound.PlaySound("ButtonClick.wav", 1)
            sg.popup("Невозможно захватить процесс, перезапустите игру!",title="ERROR!")
        else:
            winsound.PlaySound("ButtonClick.wav", 1)
            sg.popup("Can't hook process, restart the game!",title="ERROR!")
        charges = 0
        red_heart=0
        coins = 0
        bombs = 0
        keys = 0
        blue_heart=0


    pm = Pymem("isaac-ng.exe")    
    base_pymem = pm.base_address+0x804270


    def GetPtrAddr(base,offsets):
        print("govno")
        addr = pm.read_longlong(base)
        for i in offsets:
            print(i,"    ", offsets[-1])
            if i != offsets[-1]:
                addr = pm.read_longlong(addr+i)
                print(addr)
        print(addr+offsets[-1])
        return addr+offsets[-1]

    print(pm.read_int(GetPtrAddr(base_pymem, [0x4,0x1C,0x9D0,0x358,0x0,0x12B8])),"vyuio")



###############################################################################

#baza 
main()
while True:
    if win_close==1:
        charges = 0
        red_heart=0
        coins = 0
        bombs = 0
        keys = 0
        blue_heart=0
        hotkey.stop()
        break
    else:
        main()
###############################################################################