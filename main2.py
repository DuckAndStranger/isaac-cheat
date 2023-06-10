import PySimpleGUI as sg
from ReadWriteMemory import ReadWriteMemory
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound

#variables
pointers = {}
check = {"coins": 0, 'bombs': 0, 'keys': 0, 'red_hearts': 0, "charges": 0, 'dmg': 0, "blue_hearts": 0, "active_item": 0,"coin_hearts":0}
language = "ru"
win_close = False
###############################################################################

#ui
sg.theme('DarkAmber')
def layout(language):
    if language == "ru":
        main_window_layout = [  
        [sg.Text("Только целые числа",s=49),sg.Button("Hook",key="new_run",s=6),sg.Button("RU/EN",key = "Change_language",s=5)],
        [sg.Text('Монеты',s=8), sg.InputText(),sg.Button("Изменить",key="Change_coins"),sg.Button("∞ 99",key="inf_coins",s=4)],
        [sg.Text('Бомбы',s=8), sg.InputText(),sg.Button("Изменить",key="Change_bombs"),sg.Button("∞ 99",key="inf_bombs",s=4)],
        [sg.Text('Ключи',s=8), sg.InputText(),sg.Button("Изменить",key="Change_keys"),sg.Button("∞ 99",key="inf_keys",s=4)],
        [sg.Text("ID Активки",s=8),sg.InputText(),sg.Button("Изменить",key="Change_active_item"),sg.Button("D6",key="give_d6",s=4)],
        [sg.Frame("",[[sg.Text("Left ctrl + 1 - Hook",s=32),sg.Text("Left ctrl + 6 - Бесконечные бомбы",s=29)],
        [sg.Text("Left ctrl + 2 - Бесконечные красные сердца",s=32),sg.Text("Left ctrl + 7 - Бесконечные ключи",s=29)],
        [sg.Text("Left ctrl + 3 - Бесконечные синие сердца",s=32),sg.Text("Left ctrl + 8 - Бесконечная энергия",s=29)],
        [sg.Text("Left ctrl + 4 - Бесконечные сердца-монеты",s=32),sg.Text("Left ctrl + 9 - 100 урона",s=29)],
        [sg.Text("Left ctrl + 5 - Бесконечные монеты")]])],
        [sg.Button("Бесконечная энергия",key="inf_charges"),sg.Button("100 Урона",key="100 Damage",s=13),sg.Button("Бесконечные сердца-монеты",key="inf_coin_heart")],
        [sg.Button("Бесконечные красные сердца",key="inf_red_heart"),sg.Button("Бесконечные синие сердца",key="inf_blue_heart",s=21)],
        [sg.Text("")],
        [sg.Button('Выход',key="Exit"),sg.Text("",s=35),sg.Text("Made by GAVKOSHMIG Inc.")]]
    else:
        main_window_layout = [  
        [sg.Text("Only integer numbers",s=49),sg.Button("Hook",key="new_run",s=6),sg.Button("RU/EN",key = "Change_language",s=5)],
        [sg.Text('Coins',s=8), sg.InputText(),sg.Button("Change",key="Change_coins"),sg.Button("Inf 99",key="inf_coins",s=4)],
        [sg.Text('Bombs',s=8), sg.InputText(),sg.Button("Change",key="Change_bombs"),sg.Button("Inf 99",key="inf_bombs",s=4)],
        [sg.Text('Keys',s=8), sg.InputText(),sg.Button("Change",key="Change_keys"),sg.Button("Inf 99",key="inf_keys",s=4)],
        [sg.Text("Active item ID",s=10),sg.InputText(s=43),sg.Button("Change",key="Change_active_item"),sg.Button("D6",key="give_d6",s=4)],
        [sg.Frame("",[[sg.Text("Left ctrl + 1 - Hook",s=28),sg.Text("Left ctrl + 6 - Inf bombs",s=32)],
        [sg.Text("Left ctrl + 2 - Inf red hearts",s=28),sg.Text("Left ctrl + 7 - Inf keys",s=32)],
        [sg.Text("Left ctrl + 3 - Inf blue hearts",s=28),sg.Text("Left ctrl + 8 - Inf active item",s=32)],
        [sg.Text("Left ctrl + 4 - Inf coins hearts",s=28),sg.Text("Left ctrl + 9 - 100 Dmg")],
        [sg.Text("Left ctrl + 5 - Inf coins")]])],
        [sg.Button("Inf active item charge",key="inf_charges"),sg.Button("100 Damage",key="100 Damage",s=13),sg.Button("Inf coins hearts",key="inf_coin_heart")],
        [sg.Button("Inf red hearts",key="inf_red_heart"),sg.Button("Inf blue hearts",key="inf_blue_heart",s=19)],
        [sg.Text("")],
        [sg.Button('Exit',key="Exit"),sg.Text("",s=35),sg.Text("Made by GAVKOSHMIG Inc.")]]
    return sg.Window("Isaac's cheats",main_window_layout)
###############################################################################

#funcs
def writei(name, count):
    global process
    process.write(pointers[name],count)

def languageChange():
    global window, language
    window.close()
    if language == "ru":
        language = "en"
        window = (layout(language))
    else:
        language = "ru"
        window = (layout(language))

def close():
    global win_close
    win_close = True

###############################################################################

#error window
def write_and_error_window(value,thing):
    try:
        writei(thing, int(value))
    except:
        winsound.PlaySound("ButtonClick.wav", 1)
        if language == "ru": 
            text = "Ошбика!"
        else: 
            text = "ERROR!"
        sg.popup(text, title="ERROR!")

###############################################################################

#class
class Changeable:
    def __init__(self, name, num = 99) -> None:
        self.name = name
        self.num = num
    def infWrite(self):
        global check
        if check[self.name] == 0:
            check[self.name] = 1
            def everlasting():
                global check
                while check[self.name] == 1:
                        writei(self.name, self.num)
                        sleep(1)
            Thread(target=everlasting,daemon=True).start()
        elif check[self.name] == 1:
            check[self.name] = 0
    def write(self, value):
        try:
            writei(self.name, int(value))
        except:
            winsound.PlaySound("ButtonClick.wav", 1)
            if language == "ru": 
                sg.popup("Ошибка!", title="Ошибка!")
            else:
                sg.popup("Error!",title="Error!")

coins = Changeable("coins")
bombs = Changeable("bombs")
keys = Changeable("keys")
red_hearts = Changeable("red_hearts",24)
blue_hearts = Changeable("blue_hearts",12)
coin_hearts = Changeable("coin_hearts",24)
charge = Changeable("charges")
dmg = Changeable("dmg", 1120403000)
active = Changeable("active_item")
###############################################################################

#window logic
window = (layout(language))
def main():
    global window
    event, values = window.read(timeout=10)
    if values == None:
        values = [None, None, None, None]

    eventFunc = {
        "inf_coins": coins.infWrite,
        "inf_bombs": bombs.infWrite,
        "inf_keys": keys.infWrite,
        "inf_red_heart": red_hearts.infWrite,
        "inf_coin_heart": coin_hearts.infWrite,
        "inf_charges": charge.infWrite,
        "100 Damage": dmg.infWrite,
        "inf_blue_heart": blue_hearts.infWrite,
        "Change_coins": [coins.write, values[0]],
        "Change_bombs": [bombs.write, values[1]],
        "Change_keys": [keys.write, values[2]],
        "Change_active_item": [active.write, values[3]],
        "give_d6": [active.write, 105],
        "inf_coins_herts":coin_hearts.infWrite,
        "new_run":  inf_hook,
        "Change_language": languageChange,
        "Exit": close,
        sg.WIN_CLOSED:close
    }
    if event == '__TIMEOUT__':
        pass
    elif type(eventFunc[event]) == list:
        eventFunc[event][0](eventFunc[event][1])
    else:
        eventFunc[event]()
###############################################################################


###############################################################################

#process hook and pointers
def inf_hook():
    global process
    try:
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
        if pointers["coins"] == 4792:
            if language == "ru":
                winsound.PlaySound("ButtonClick.wav", 1)
                sg.popup("Невозможно захватить процесс, перезапустите игру/забег!",title="ERROR!")
            else:
                winsound.PlaySound("ButtonClick.wav", 1)
                sg.popup("Can't hook process, restart the game/the run!",title="ERROR!")
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

#baza 
# while True:
#     main()
#     if win_close == True:
#         break
#     else: main()
############################################################################## 1112014848






import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,  QMainWindow
from Interface_RU2 import Ui_MainWindow



Form,  _ = uic.loadUiType("Interface_RU2.ui")

class Ui(QMainWindow,Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.Inf_blue_hearts.clicked.connect(self.pushButton_pressed)
    def pushButton_pressed(self):
        print(self,"pressed")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec())
