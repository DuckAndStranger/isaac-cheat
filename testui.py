import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication,  QMainWindow
from Interface_RU2 import Ui_MainWindow
import main2


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




# app = QApplication(sys.argv)
# window = Window()

# ui = Ui_MainWindow()
# ui.setupUi(window)

# window.show()
# sys.exit(app.exec())