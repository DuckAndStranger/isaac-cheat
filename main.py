import PySimpleGUI as sg
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QIntValidator
from ReadWriteMemory import ReadWriteMemory
import win32process
import win32api
import psutil
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound
import sys

#variables
points = {}
check = {"coins": False, 'bombs': False, 'keys': False, 'red_hearts': False, "charges": False, 'dmgs': False, "blue_hearts": False, "active_item": False}
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

#process hook
def process_hook():
    global process,base_address
    my_pid = None
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
    rwm = ReadWriteMemory()
    process = rwm.get_process_by_name("isaac-ng.exe")
    process.open()
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
        main_window_layout = [  [sg.Text("Only integer numbers",s=57),sg.Button("RU/EN",key = "Change_language",s=6)],
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

def writei(name, count):
    process.write(points[name],count)

def languageChange():
    window.close()
    if language == "ru":
        language = "en"
        window = (layout(language))
    else:
        language = "ru"
        window = (layout(language))

def close():
    global win_close
    win_close=1
    #window.close()    

###############################################################################

#error window
def write_and_error_window(value,thing):
    try:
        writei(thing, int(value))
    except:
        winsound.PlaySound("ButtonClick.wav", 1)
        text = "Your input isn't integer number!"
        if language == "ru": 
            text = "Вы ввели не целое число!"
        sg.popup(text, title="ERROR!")

###############################################################################

class Changeable:
    def __init__(self, name, num = 99, line = False, checked = True) -> None:
        self.name = name
        self.num = num
        if line:
            window.create_line(name, checked)
        else:
            window.create_button(name, checked)
    def infWrite(self):
        global check
        if check[self.name] == 0:
            check[self.name] = 1
            def everlasting():
                global check
                while check[self.name] == 1:
                        writei(self.name, self.num)
                        sleep(1)
            Thread(target=everlasting).start()
        elif check[self.name] == 1:
            check[self.name] = 0
    def write(self, value):
        try:
            writei(self.name, int(value))
        except:
            winsound.PlaySound("ButtonClick.wav", 1)
            text = "Your input isn't integer number!"
            if language == "ru": 
                text = "Вы ввели не целое число!"
            sg.popup(text, title="ERROR!")



###############################################################################
#-----НОВОЕ ОКНО------

#Кнопка ого
class Button(QPushButton):
    def __init__(self, name, checked = True):
        super(Button, self).__init__()
        self.name = name
        self.setText(name)
        if checked:
            self.setCheckable(True)
        self.clicked.connect(self.the_button_was_toggled)
        if checked:
            try:
                self.setChecked(check[self.name])
            except:
                pass

    def the_button_was_toggled(self, checked):
        check[self.name] = checked
        print(self.name, check[self.name])

class SpecialButton(QPushButton):
    def __init__(self, name):
        super(QPushButton, self).__init__()
        self.setText(name)
        self.setBaseSize(10, 10)
        if name == "Hook":
            self.clicked.connect(self.hook)
        else:
            self.clicked.connect(self.lang)
        
    def hook(self):
        pass

    def lang(self):
        pass

class LineEdit(QHBoxLayout):
    def __init__(self, name, checked=True):
        super(QHBoxLayout, self).__init__()
        self.name = name
        self.input = QLineEdit()
        self.onlyInt = QIntValidator()
        self.onlyInt.setRange(0, 999)
        self.input.setValidator(self.onlyInt)
        self.input.setFixedWidth(150)
        self.addWidget(self.input)
        self.button1 = QPushButton("Изменить")
        self.button2 = Button(name, checked)
        self.button1.clicked.connect(self.get)
        self.addWidget(self.button1)
        self.addWidget(self.button2)

    def get(self):
        text = self.input.text()
        print(text)

#Класс окна, все настраиваем тут
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Isaac Cheats")
        self.setFixedSize(330, 290)
        self.layout = QVBoxLayout()
        self.button_checked = {}

    def create_button(self, name, checked = True):
        try:
            self.button_checked[name] = False
        except:
            pass
        button = Button(name, checked)
        self.layout.addWidget(button)

    def create_line(self, name, checked):
        self.button_checked[name] = False
        line = LineEdit(name, checked)
        self.layout.addLayout(line)

    def initiate(self):
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)

app = QApplication(sys.argv)
window = MainWindow()

fbuttons = QGridLayout()
hook = SpecialButton("Hook")
lang = SpecialButton("EN/RU")
fbuttons.addWidget(hook)
fbuttons.addWidget(lang)
window.addLayout(fbuttons)

coin = Changeable("coins", line=True)
bomb = Changeable("bombs", line=True)
key = Changeable("keys", line=True)
active = Changeable("active_item", line=True, checked=False)
red_hearts = Changeable("red_hearts", 24)
charge = Changeable("charges", 6)
blue_hearts = Changeable("blue_hearts", 8)
dmgs = Changeable("dmgs", 1120403000)

window.initiate()
window.show()
app.exec() #Открытие

###############################################################################

#window logic
#window = (layout(language))
def main():
    global coins_point,address,process,process_hook_status,win_close
    global process,base_address
    global coins, bombs,keys,win_close,process_hook_status,language,window
    #event, values = window.read(timeout=10)

    #if values == None:
    values = [None, None, None, None]
    event = None

    eventFunc = {
        "inf_coins": coin.infWrite,
        "inf_bombs": bomb.infWrite,
        "inf_keys": key.infWrite,
        "inf_red_heart": red_hearts.infWrite,
        "inf_charges": charge.infWrite,
        "100 Damage": dmgs.infWrite,
        "inf_blue_heart": blue_hearts.infWrite,
        "Change_coins": [coin.write, values[0]],
        "Change_bombs": [bomb.write, values[1]],
        "Change_keys": [key.write, values[2]],
        "Change_active_item": [active.write, values[3]],
        "give_d6": [active.write, 105],
        "new_run":  inf_hook,
        "Change_language": languageChange,
        "Exit": close,
        sg.WIN_CLOSED: close
    }

    if event == '__TIMEOUT__':
        pass
    elif type(eventFunc[event]) == list:
        eventFunc[event][0](eventFunc[event][1])
    else:
        eventFunc[event]()
  
###############################################################################

#hotkeys
def hotkeys():
    global hotkey
    with keyboard.GlobalHotKeys({
        "<ctrl>+1":coin.infWrite,
        "<ctrl>+2":bomb.infWrite,
        "<ctrl>+3":key.infWrite,
        "<ctrl>+4":dmgs.infWrite,
        "<ctrl>+5":red_hearts.infWrite,
        "<ctrl>+6":blue_hearts.infWrite,
        "<ctrl>+7":charge.infWrite}) as hotkey:
        hotkey.join()
#Thread(target=hotkeys).start()

###############################################################################

#process hook and pointers
def inf_hook():
    try:
        global coins_point,address,process,process_hook_status,win_close
        global charges,red_heart,blue_heart,coins,bombs,keys,base_address, points
        my_pid = None
        pids = None
        ps = None
        pids = psutil.pids()
        for pid in pids:
            ps = psutil.Process(pid) 
            if "isaac-ng.exe" in ps.name():
                my_pid = ps.pid
        print(my_pid)
        PROCESS_ALL_ACCESS = 0x1F0FFF
        processHandle = win32api.OpenProcess(PROCESS_ALL_ACCESS, False, my_pid)
        modules = win32process.EnumProcessModules(processHandle)
        processHandle.close()
        base_address = modules[0]
        rwm = ReadWriteMemory()
        process = rwm.get_process_by_name("isaac-ng.exe")
        process.open()
        address = base_address+0x804270
        points["coins"] = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x358,0x0,0x12B8])
        process_hook_status = 1
        points["bombs"] = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x12B4])
        points["keys"] = process.get_pointer(address, offsets=[0x4,0x1C,0xBBC,0x16C,0x0,0x12AC])
        points["dmgs"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x23C,0x16C,0x0,0x13B8])
        points["red_hearts"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9F0,0x23C,0x16C,0x0,0x1294])
        points["charges"] = process.get_pointer(address,offsets=[0x4,0x0,0x4,0x1C,0xCF8,0x0,0x14C8])
        points["active_item"] = process.get_pointer(address,offsets=[0x8,0x1C,0x9F0,0x30,0x358,0x0,0x14C4])
        points["blue_hearts"] = process.get_pointer(address,offsets=[0x4,0x1C,0x9D0,0x50,0x358,0x0,0x129C])
        if coins_point == 4792:
            if language == "ru":
                winsound.PlaySound("ButtonClick.wav", 1)
                sg.popup("Невозможно захватить процесс, перезапустите игру!",title="ERROR!")
            else:
                winsound.PlaySound("ButtonClick.wav", 1)
                sg.popup("Can't hook process, restart the game!",title="ERROR!")
            for i in check:
                i = 0
    except:
        pass

###############################################################################

#baza 
main()
# while True:
#     if win_close==1:
#         for i in check:
#             i = 0
#         #hotkey.stop()
#         break
#     else:
#         main()
###############################################################################