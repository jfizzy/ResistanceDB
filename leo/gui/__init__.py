import sys
from PyQt5.QtWidgets import QDialog, QApplication
from gui.leo_gui import Ui_MainWindow

def main():
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_MainWindow
    ui.setupUi(window)

if __name__ == "__main__":
    main()