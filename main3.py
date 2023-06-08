import PySimpleGUI as sg
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QWidget, QPushButton, QMainWindow, QLineEdit, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QIntValidator
from ReadWriteMemory import ReadWriteMemory
from threading import Thread
from pynput import keyboard
from time import sleep
import winsound
import sys

#variables
points = {}
check = {"coins": 0, 'bombs': 0, 'keys': 0, 'red_hearts': 0, "charges": 0, 'dmgs': 0, "blue_hearts": 0, "active_item": 0}
coins_point=0
language = "ru"
dmg =0
red_heart=0
coins = 0
bombs = 0
keys = 0
win_close=0
charges=0
blue_heart=0
process_hook_stop=0



def inf_hook():
    try:
        global coins_point,process,points
        print("govno2")
        process = ReadWriteMemory().get_process_by_name("isaac-ng.exe")
        process.open()
        address = process.get_base_address()+0x804270        
        points["coins"] = process.get_pointer(address, offsets=[0x4,0x1C,0x9D0,0x358,0x0,0x12B8])
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

def writei(name, count):
    process.write(points[name],count)

class Changeable:
    def writei(name, count):
        process.write(points[name],count)
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
            if language == "ru": 
                sg.popup("Ошибка!", title="Ошибка!")
            else:
                sg.popup("Error!",title="Error!")


###############################################################################
#-----НОВОЕ ОКНО------

#Кнопка ого
# class Button(QPushButton):
#     def __init__(self, name, checked = True):
#         super(Button, self).__init__()
#         self.name = name
#         self.setText(name)
#         if checked:
#             self.setCheckable(True)
#         self.clicked.connect(self.the_button_was_toggled)
#         if checked:
#             try:
#                 self.setChecked(check[self.name])
#             except:
#                 pass

#     def the_button_was_toggled(self, checked):
#         check[self.name] = checked
#         print(self.name, check[self.name])

# class SpecialButton(QPushButton):
#     def __init__(self, name):
#         super(QPushButton, self).__init__()
#         self.setText(name)
#         self.setBaseSize(10, 10)
#         if name == "Hook":
#             self.clicked.connect(self.hook)
#         else:
#             self.clicked.connect(self.lang)
        
#     def hook(self):
#         inf_hook()
#         print("govno1")

#     def lang(self):
#         pass

# class LineEdit(QHBoxLayout):
#     def __init__(self, name, checked=True):
#         super(QHBoxLayout, self).__init__()
#         self.name = name
#         self.input = QLineEdit()
#         self.onlyInt = QIntValidator()
#         self.onlyInt.setRange(0, 999)
#         self.input.setValidator(self.onlyInt)
#         self.input.setFixedWidth(150)
#         self.addWidget(self.input)
#         self.button1 = QPushButton("Изменить")
#         self.button2 = Button(name, checked)
#         self.button1.clicked.connect(self.get)
#         self.addWidget(self.button1)
#         self.addWidget(self.button2)

#     def get(self):
#         text = self.input.text()
#         print(text)

# #Класс окна, все настраиваем тут
# class MainWindow(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Isaac Cheats")
#         self.layout = QVBoxLayout()
#         self.button_checked = {}

#     def create_button(self, name, checked = True):
#         try:
#             self.button_checked[name] = False
#         except:
#             pass
#         button = Button(name, checked)
#         self.layout.addWidget(button)

#     def create_line(self, name, checked):
#         self.button_checked[name] = False
#         line = LineEdit(name, checked)
#         self.layout.addLayout(line)

#     def initiate(self):
#         self.widget = QWidget()
#         self.widget.setLayout(self.layout)
#         self.setCentralWidget(self.widget)

#     def addLayout(self, layout):
#         self.layout.addLayout(layout)

# app = QApplication(sys.argv)
# window = MainWindow()

# fbuttons = QGridLayout()
# hook = SpecialButton("Hook")
# lang = SpecialButton("EN/RU")
# fbuttons.addWidget(hook)
# fbuttons.addWidget(lang)
# window.addLayout(fbuttons)

coin = Changeable("coins", line=True)
bomb = Changeable("bombs", line=True)
key = Changeable("keys", line=True)
active = Changeable("active_item", line=True, checked=False)
red_hearts = Changeable("red_hearts", 24)
charge = Changeable("charges", 6)
blue_hearts = Changeable("blue_hearts", 8)
dmgs = Changeable("dmgs", 1120403000)

# window.initiate()
# window.show()
# app.exec() #Открытие

###############################################################################

#window logic
#window = (layout(language))
# def main():
#     global coins_point,process,win_close
#     global process
#     global coins, bombs,keys,win_close,language,window
#     #event, values = window.read(timeout=10)

#     #if values == None:
#     values = [None, None, None, None]
#     event = None

#     eventFunc = {
#         "inf_coins": coin.infWrite,
#         "inf_bombs": bomb.infWrite,
#         "inf_keys": key.infWrite,
#         "inf_red_heart": red_hearts.infWrite,
#         "inf_charges": charge.infWrite,
#         "100 Damage": dmgs.infWrite,
#         "inf_blue_heart": blue_hearts.infWrite,
#         "Change_coins": [coin.write, values[0]],
#         "Change_bombs": [bomb.write, values[1]],
#         "Change_keys": [key.write, values[2]],
#         "Change_active_item": [active.write, values[3]],
#         "give_d6": [active.write, 105],
#         "new_run":  inf_hook,
#         "Change_language": languageChange,
#         "Exit": close,
#         sg.WIN_CLOSED: close
#     }

#     if event == '__TIMEOUT__':
#         pass
#     elif type(eventFunc[event]) == list:
#         eventFunc[event][0](eventFunc[event][1])
#     else:
#         eventFunc[event]()
  
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
Thread(target=hotkeys).start()

###############################################################################

#process hook and pointers
