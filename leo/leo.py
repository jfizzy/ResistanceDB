import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui.leo_gui import Ui_MainWindow

class ApplicationWindow(QtWidgets.QMainWindow):
    ICON = os.path.join(os.path.abspath(os.path.dirname(__file__)), "gui", "leo-icon.png")

    def __init__(self, parent):
        super(ApplicationWindow, self).__init__()
        self.parent = parent
        self.main_window = Ui_MainWindow(self)
        self.main_window.setupUi(self)
        #self._shutdown = False
        self.setWindowIcon(QtGui.QIcon(self.ICON))

    def shut_er_down(self):
        QtWidgets.QMainWindow.close(self)

    def closeEvent(self, event):
        self.main_window.shutdown()


def main():
    app = QApplication(sys.argv)
    window = ApplicationWindow(app)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()