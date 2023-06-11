from ReadWriteMemory import ReadWriteMemory
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,  QMainWindow, QDialog
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from pymem import Pymem
import numpy as np

#variables
pointers = {}
check = {"coins": False, 'bombs': False, 'keys': False, 'red_hearts': False, "charges": False, 'dmg': False, "blue_hearts": False, "active_item": False,"coin_hearts":False}
language = "ru"


###############################################################################


#class
class Changeable:
    def __init__(self, name, num = 99) -> None:
        self.name = name
        self.num = num
    def infWrite(self,f=False):
        global check
        if check[self.name] == False:
            check[self.name] = False
            def everlasting():
                global check
                if f == False:
                    while check[self.name] == False:
                            pm.write_int(pointers[self.name],int(self.num))
                            sleep(1)
                else:
                    while check[self.name] == False:
                            print(self.num)
                            pm.write_float(pointers[self.name],float(self.num))
                            sleep(1)                    
            Thread(target=everlasting,daemon=True).start()
        else:
            check[self.name] = False

    def write(self, value, f=False):
        try:
            if f==False:
                pm.write_int(pointers[self.name],int(value))
            else:
                pm.write_float(pointers[self.name],float(value))
        except:
            winsound.PlaySound("ButtonClick.wav", 1)
            if language == "ru": 
                error_ru.exec()
            else:
                error_en.exec()

coins = Changeable("coins")
bombs = Changeable("bombs")
keys = Changeable("keys")
red_hearts = Changeable("red_hearts",24)
blue_hearts = Changeable("blue_hearts",12)
coin_hearts = Changeable("coin_hearts",24)
charge = Changeable("charges")
dmg = Changeable("dmg")
active = Changeable("active_item")


###############################################################################  014E99BE 5099BE

#process hook and pointers
def inf_hook():
    global process,pm
    try:
        pm = Pymem("isaac-ng.exe")
        process = ReadWriteMemory().get_process_by_name("isaac-ng.exe")
        process.open()
        address = process.get_base_address()+0x804270 
        pointers["coins"] = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x358,0x0,0x12B8])
        pointers["bombs"] = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x12B4])
        pointers["keys"] = process.get_pointer(address, offsets=[0x4,0x1C,0xBBC,0x16C,0x0,0x12AC])
        pointers["dmg"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x13B8])
        pointers["red_hearts"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9F0,0x23C,0x16C,0x0,0x1294])
        pointers["charges"] = process.get_pointer(address,offsets=[0x4,0x0,0x4,0x1C,0xCF8,0x0,0x14C8])
        pointers["active_item"] = process.get_pointer(address,offsets=[0x8,0x1C,0x9F0,0x30,0x358,0x0,0x14C4])
        pointers["blue_hearts"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x50,0x358,0x0,0x129C])
        pointers["coin_hearts"] = process.get_pointer(address,offsets=[0x8,0x3c,0x1c,0x9D0,0x358,0x0,0x1294])



        winsound.PlaySound("ButtonClick.wav", 1)
        if pointers["coins"] == 4792:
            if language == "ru":
                hook_error_ru.exec()
            else:
                hook_error_en.exec()
    except:
        pass

###############################################################################

#hotkeys
def hotkeys():
    global hotkey
    with keyboard.GlobalHotKeys({
        "<ctrl>+1":inf_hook,
        "<ctrl>+2":red_hearts.infWrite,
        "<ctrl>+3":blue_hearts.infWrite,
        "<ctrl>+4":coin_hearts.infWrite,
        "<ctrl>+5":coins.infWrite,
        "<ctrl>+6":bombs.infWrite,
        "<ctrl>+7":keys.infWrite,
        "<ctrl>+8":charge.infWrite,
        "<ctrl>+9":dmg.infWrite}) as hotkey:
        hotkey.join()
Thread(target=hotkeys,daemon=True).start()

###############################################################################

def languageChange1():
    global language,Main_WindowRU,Main_WindowEN
    if language == "ru":
        Main_WindowRU.close()
        Main_WindowEN.show()
        language = "eng"
    else:
        Main_WindowEN.close()
        Main_WindowRU.show()
        language = "ru"

Form_Main_WindowRU,  Main_WindowRU = uic.loadUiType("Interface_RU14.ui")
Form_Main_Window_EN,  Main_WindowEN = uic.loadUiType("Interface_EN7.ui")
Form_ErrorEN, WErrorEN = uic.loadUiType("Error_EN2.ui")
Form_ErrorRU, WErrorRU = uic.loadUiType("Error_RU2.ui")
Form_Hook_ErrorEN, W_Hook_ErrorEN = uic.loadUiType("Error_Hook_EN2.ui")
Form_Hook_ErrorRU, W_Hook_ErrorRU = uic.loadUiType("Error_Hook_RU2.ui")

class MainUIWindowRU(QMainWindow, Form_Main_WindowRU):
    def __init__(self):
        super(MainUIWindowRU, self).__init__()
        self.setupUi(self)
        # self.Inf_blue_hearts.clicked.connect(blue_hearts.infWrite)
        # self.D6_btn.clicked.connect(lambda: active.write(105))
        # self.Dmg_btn.clicked.connect(dmg.infWrite)
        # self.Inf_energy.clicked.connect(charge.infWrite)
        # self.Inf_hearts_coins.clicked.connect(coin_hearts.infWrite)
        # self.Inf_red_hearts.clicked.connect(red_hearts.infWrite)
        # self.Infinity_bombs.clicked.connect(bombs.infWrite)
        # self.Infinity_coins.clicked.connect(coins.infWrite)
        # self.Infinity_keys.clicked.connect(keys.infWrite)
        # self.Hook_btn.clicked.connect(inf_hook)
        # self.Exit_btn.clicked.connect(sys.exit)
        # self.Language_btn.clicked.connect(languageChange1)


        # coins_input = self.Input_coins
        # coins_input.setValidator(QIntValidator())
        # self.Change_coins.clicked.connect(lambda: coins.write(coins_input.text()))

        # bombs_input = self.Input_bombs
        # bombs_input.setValidator(QIntValidator())

        # self.Change_bombs.clicked.connect(lambda: bombs.write(bombs_input.text()))

        # keys_input = self.Input_keys
        # keys_input.setValidator(QIntValidator())
        # self.Change_keys.clicked.connect(lambda: keys.write(keys_input.text()))

        # active_input = self.Input_items
        # active_input.setValidator(QIntValidator())
        # self.Change_items.clicked.connect(lambda: active.write(active_input.text()))

        # dmg_input = self.Input_items_2
        # dmg_input.setValidator(QDoubleValidator())
        # self.Dmg_btn_2.clicked.connect(lambda: dmg.write(dmg_input.text(),f=True))


        self.checkBox.stateChanged.connect(coins.infWrite)




class MainUIWindowEN(QMainWindow, Form_Main_Window_EN):
    def __init__(self):
        super(MainUIWindowEN, self).__init__()
        self.setupUi(self)
        self.Inf_blue_hearts.clicked.connect(blue_hearts.infWrite)
        self.D6_btn.clicked.connect(lambda: active.write(105))
        self.Dmg_btn.clicked.connect(dmg.infWrite)
        self.Inf_energy.clicked.connect(charge.infWrite)
        self.Inf_hearts_coins.clicked.connect(coin_hearts.infWrite)
        self.Inf_red_hearts.clicked.connect(red_hearts.infWrite)
        self.Infinity_bombs.clicked.connect(bombs.infWrite)
        self.Infinity_coins.clicked.connect(coins.infWrite)
        self.Infinity_keys.clicked.connect(keys.infWrite)
        self.Hook_btn.clicked.connect(inf_hook)
        self.Exit_btn.clicked.connect(sys.exit)
        self.Language_btn.clicked.connect(languageChange1)
        coins_input = self.Input_coins
        coins_input.setValidator(QIntValidator())
        self.Change_coins.clicked.connect(lambda: coins.write(coins_input.text()))

        bombs_input = self.Input_bombs
        bombs_input.setValidator(QIntValidator())

        self.Change_bombs.clicked.connect(lambda: bombs.write(bombs_input.text()))

        keys_input = self.Input_keys
        keys_input.setValidator(QIntValidator())
        self.Change_keys.clicked.connect(lambda: keys.write(keys_input.text()))

        active_input = self.Input_items
        active_input.setValidator(QIntValidator())
        self.Change_items.clicked.connect(lambda: active.write(active_input.text()))








class Error_Window_EN(QDialog, Form_ErrorEN):
    def __init__(self):
        super(Error_Window_EN, self).__init__()
        self.setupUi(self)
        self.OK_btn.clicked.connect(self.close)

class Error_Window_RU(QDialog, Form_ErrorRU):
    def __init__(self):
        super(Error_Window_RU, self).__init__()
        self.setupUi(self)
        self.OK_btn.clicked.connect(self.close)    

class Hook_Error_Window_EN(QDialog, Form_Hook_ErrorEN):
    def __init__(self):
        super(Hook_Error_Window_EN, self).__init__()
        self.setupUi(self)
        self.OK_btn.clicked.connect(self.close)

class Hook_Error_Window_RU(QDialog, Form_Hook_ErrorRU):
    def __init__(self):
        super(Hook_Error_Window_RU, self).__init__()
        self.setupUi(self)
        self.OK_btn.clicked.connect(self.close)    


if language =="ru":
    app = QApplication(sys.argv)
    Main_WindowRU = MainUIWindowRU()
    Main_WindowEN = MainUIWindowEN()
    error_en = Error_Window_EN()
    error_ru = Error_Window_RU()
    hook_error_ru = Hook_Error_Window_RU()
    hook_error_en = Hook_Error_Window_EN()
    Main_WindowRU.show()
    sys.exit(app.exec())

