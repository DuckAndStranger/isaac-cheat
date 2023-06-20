from ReadWriteMemory import *
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,  QMainWindow, QDialog
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from pymem import Pymem
import webbrowser


#variables
pointers = {}
check = {"coins": False, 'bombs': False, 'keys': False, 'red_hearts': False, "charges": False, 'dmg': False, "blue_hearts": False, "active_item": False,"coin_hearts":False,"spd":False,"shot_spd": False}
language = "ru"


############################################################################### 13A8


#class
class Changeable:
    def __init__(self, name, num = 99) -> None:
        self.name = name
        self.num = num
    def infWrite(self,f=False):
        global check
        if check[self.name] == False:
            check[self.name] = True
            def everlasting():
                global check
                if f == False:
                    self.num = int(self.num)
                    while check[self.name] == True:
                            pm.write_int(pointers[self.name],self.num)
                            sleep(0.5)
                else:
                    try:
                        value =float(value.replace(",","."))
                    except:
                        value=float(value)
                    while check[self.name] == True:
                            pm.write_float(pointers[self.name],self.num)
                            sleep(0.5)                    
            Thread(target=everlasting,daemon=True).start()
        else:
            check[self.name] = False

    def write(self, value, f=False):
        try:
            if f==False:
                value = int(value)
                pm.write_int(pointers[self.name],value)
            else:
                try:
                    value = float(value.replace(",","."))
                except:
                    value=float(value)
                pm.write_float(pointers[self.name],value)
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
spd = Changeable("spd")
shot_spd= Changeable("shot_spd")
trinket = Changeable("trinket")
luck = Changeable("luck")
tears = Changeable("tears")


###############################################################################  014E99BE 5099BE 0x15E8 13A8

#process hook and pointers
def inf_hook():
    global process,pm,address
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
        pointers["coin_hearts"] = process.get_pointer(address,offsets=[0x4,0x1C,0xBDC,0x30,0x16C,0x0,0x1294])
        pointers["spd"] = process.get_pointer(address,offsets=[0x4,0x1C,0xCF8,0x0,0x39C,0x258,0xF18])
        pointers["shot_spd"] = process.get_pointer(address,offsets=[0x8,0x1C,0x9F0,0x21C,0x16C,0x0,0x13AC])
        pointers["trinket"] = process.get_pointer(address,offsets=[0x8,0x1C,0xBBC,0x50,0x16C,0x0,0x15E8])
        pointers["luck"] = process.get_pointer(address,offsets=[0x8,0x4,0x1C,0x9F0,0x358,0x0,0x14B0])
        pointers["tears"] = process.get_pointer(address,offsets=[0x4,0x8,0x1C,0x9D0,0x358,0x0,0x13A8])



        winsound.PlaySound("ButtonClick.wav", 1)
        if pointers["coins"] == 4792:
            if language == "ru":
                hook_error_ru.exec()
            else:
                hook_error_en.exec()
    except:
        pass

############################################################################### 00B08D8E

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
        "<ctrl>+9":lambda: dmg.write(100,f=True)}) as hotkey:
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


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)






Form_Main_WindowRU,  Main_WindowRU = uic.loadUiType(resource_path("Interface_RU17.ui"))
Form_Main_Window_EN,  Main_WindowEN = uic.loadUiType(resource_path("Interface_EN7.ui"))
Form_ErrorEN, WErrorEN = uic.loadUiType(resource_path("Error_EN2.ui"))
Form_ErrorRU, WErrorRU = uic.loadUiType(resource_path("Error_RU2.ui"))
Form_Hook_ErrorEN, W_Hook_ErrorEN = uic.loadUiType(resource_path("Error_Hook_EN2.ui"))
Form_Hook_ErrorRU, W_Hook_ErrorRU = uic.loadUiType(resource_path("Error_Hook_RU2.ui"))





class MainUIWindowRU(QMainWindow, Form_Main_WindowRU):
    def __init__(self):
        super(MainUIWindowRU, self).__init__()
        self.setupUi(self)
        self.Inf_blue_hearts.clicked.connect(blue_hearts.infWrite)
        self.D6_btn.clicked.connect(lambda: active.write(105))
        self.Inf_energy.clicked.connect(charge.infWrite)
        self.Inf_hearts_coins.clicked.connect(coin_hearts.infWrite)
        self.Inf_red_hearts.clicked.connect(red_hearts.infWrite)
        self.Infinity_bombs.clicked.connect(bombs.infWrite)
        self.Infinity_coins.clicked.connect(coins.infWrite)
        self.Infinity_keys.clicked.connect(keys.infWrite)
        self.Hook_btn.clicked.connect(inf_hook)
        self.Exit_btn.clicked.connect(sys.exit)
        self.Language_btn.clicked.connect(languageChange1)
        self.Dmg_100.clicked.connect(lambda: dmg.write(100,f=True))
        self.Trinket_btn.clicked.connect(lambda: trinket.write(23))
        self.Author_btn.clicked.connect(lambda: webbrowser.open("https://github.com/DuckAndStranger/isaac-cheat"))

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

        dmg_input = self.Input_dmg
        dmg_input.setValidator(QDoubleValidator())
        self.Change_dmg.clicked.connect(lambda: dmg.write(dmg_input.text(),f=True))

        spd_input = self.Input_spd
        spd_input.setValidator(QDoubleValidator())
        self.Change_spd.clicked.connect(lambda: spd.write(spd_input.text(),f=True))

        shot_spd_input = self.Input_shot_spd
        shot_spd_input.setValidator(QDoubleValidator())
        self.Change_shot_spd.clicked.connect(lambda: shot_spd.write(shot_spd_input.text(),f=True))

        trinket_input = self.Input_trinket
        trinket_input.setValidator(QIntValidator())
        self.Change_trinket.clicked.connect(lambda: trinket.write(trinket_input.text()))

        luck_input = self.Input_luck
        luck_input.setValidator(QDoubleValidator())
        self.Change_luck.clicked.connect(lambda: luck.write(luck_input.text(),f=True))

        tears_input = self.Input_tears
        tears_input.setValidator(QDoubleValidator())
        self.Change_tears.clicked.connect(lambda: tears.write(tears_input.text(),f=True))



class MainUIWindowEN(QMainWindow, Form_Main_Window_EN):
    def __init__(self):
        super(MainUIWindowEN, self).__init__()
        self.setupUi(self)
        self.Inf_blue_hearts.clicked.connect(blue_hearts.infWrite)
        self.D6_btn.clicked.connect(lambda: active.write(105))
        self.Inf_energy.clicked.connect(charge.infWrite)
        self.Inf_hearts_coins.clicked.connect(coin_hearts.infWrite)
        self.Inf_red_hearts.clicked.connect(red_hearts.infWrite)
        self.Infinity_bombs.clicked.connect(bombs.infWrite)
        self.Infinity_coins.clicked.connect(coins.infWrite)
        self.Infinity_keys.clicked.connect(keys.infWrite)
        self.Hook_btn.clicked.connect(inf_hook)
        self.Exit_btn.clicked.connect(sys.exit)
        self.Language_btn.clicked.connect(languageChange1)
        self.Dmg_100.clicked.connect(lambda: dmg.write(100,f=True))
        self.Trinket_btn.clicked.connect(lambda: trinket.write(23))
        self.Author_btn.clicked.connect(lambda: webbrowser.open("https://github.com/DuckAndStranger/isaac-cheat"))

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

        dmg_input = self.Input_dmg
        dmg_input.setValidator(QDoubleValidator())
        self.Change_dmg.clicked.connect(lambda: dmg.write(dmg_input.text(),f=True))

        spd_input = self.Input_spd
        spd_input.setValidator(QDoubleValidator())
        self.Change_spd.clicked.connect(lambda: spd.write(spd_input.text(),f=True))

        shot_spd_input = self.Input_shot_spd
        shot_spd_input.setValidator(QDoubleValidator())
        self.Change_shot_spd.clicked.connect(lambda: shot_spd.write(shot_spd_input.text(),f=True))

        trinket_input = self.Input_trinket
        trinket_input.setValidator(QIntValidator())
        self.Change_trinket.clicked.connect(lambda: trinket.write(trinket_input.text()))

        luck_input = self.Input_luck
        luck_input.setValidator(QDoubleValidator())
        self.Change_luck.clicked.connect(lambda: luck.write(luck_input.text(),f=True))

        tears_input = self.Input_tears
        tears_input.setValidator(QDoubleValidator())
        self.Change_tears.clicked.connect(lambda: tears.write(tears_input.text(),f=True))






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