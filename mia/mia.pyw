from PyQt5 import QtWidgets, QtGui
from gui.gui import Ui_MainWindow
import sys
from mia_backend.mia_manager import MiaManager

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ApplicationWindow, self).__init__()
        self.parent = parent
        self.main_window = Ui_MainWindow(self)
        self.main_window.setupUi(self)
        self.main_window.loaded()
        self._shutdown = False
        self.setWindowIcon(QtGui.QIcon("gui/mia.gif"))

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