#! C:\Users\Tyrone\code\ResistanceDB\mia\.venv\Scripts\pythonw.exe

from PyQt5 import QtWidgets, QtGui
from gui.gui import Ui_MainWindow
import os
import sys
from mia_backend.mia_manager import MiaManager

class ApplicationWindow(QtWidgets.QMainWindow):
    ICON = os.path.join(os.path.abspath(os.path.dirname(__file__)), "gui", "mia.gif")

    def __init__(self, parent):
        super(ApplicationWindow, self).__init__()
        self.parent = parent
        self.main_window = Ui_MainWindow(self)
        self.main_window.setupUi(self)
        self.main_window.loaded()
        self._shutdown = False
        self.setWindowIcon(QtGui.QIcon(self.ICON))

    def shut_er_down(self):
         self._shutdown = True
         self.parent.setQuitOnLastWindowClosed(True)
         QtWidgets.QMainWindow.close(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    #window = QWidgets.QDialog()
    #app.setWindowFlags(QtCore.Qt.Tool)
    app.setQuitOnLastWindowClosed(False)
    application = ApplicationWindow(app)
    #application.setWindowIcon(QtWidgets.QIcon("mia_backend/mia.gif"))
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()