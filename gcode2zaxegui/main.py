
import sys
from ui import ui_design
from styles import Styles
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
    

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Gcode 2 Zaxe")
        self.setStyleSheet("background-color: rgba(210, 210, 210, 0.8);")
       
        self.startMainMenu()

    def startMainMenu(self):
        self.window = ui_design(self)
        self.setCentralWidget(self.window)
        self.showMaximized()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()