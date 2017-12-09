# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'leo.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    ICON = os.path.join(os.path.abspath(os.path.dirname(__file__)), "leo-icon.png")

    def __init__(self, parent):
        """ """
        self.parent = parent
        self.systemTray = QtWidgets.QSystemTrayIcon()

        systrayMenu = QtWidgets.QMenu()
        openAction = systrayMenu.addAction("open")
        openAction.triggered.connect(self.systray_open)

        closeAction = systrayMenu.addAction("close")
        closeAction.triggered.connect(self.systray_close)

        self.systemTray.setIcon(QtGui.QIcon(self.ICON))
        #self.systemTrayIcon.setVisible(True)

        self.systemTray.setToolTip("leo")
        self.systemTray.activated.connect(self.systray_clicked)

        self.systemTray.setContextMenu(systrayMenu)
        self.systemTray.show()

    def systray_open(self):
        """ """

    def systray_close(self):
        """ """

    def systray_clicked(self, event):
        """ user clicked on system tray icon, ensure it wasn't a context menu click, otherwise show """
        if event != QtWidgets.QSystemTrayIcon.Context:
            self.parent.show()
            self.parent.showNormal()

    def raw_peak_btn_clicked(self):
        """ pick raw peaks location """
        print("pick raw peak file")
        file_name = QtWidgets.QFileDialog.getOpenFileName()
        if file_name:
           self.rawPeakLineEdit.setText(file_name[0].replace("/","\\"))

    def output_loc_clicked(self):
        """ pick output locaiton """
        file_name = self.getSaveFileLocation()
        if file_name:
           self.outputLocationLineEdit.setText(file_name[0].replace("/","\\"))

    def condensed_btn_clicked(self):
        """ pick condensed output location """
        file_name = self.getSaveFileLocation()
        if file_name:
            self.condensedOutputLineEdit.setText(file_name[0].replace("/","\\"))

    def getSaveFileLocation(self):
        dlg = QtWidgets.QFileDialog()
        file_name = dlg.getSaveFileName(None, None, None, "CSV Delimited Data File (*.csv)");
        return file_name;

    def parse_btn_clicked(self):
        """ """
        minMz = self.minMZSpinBox.value()
        maxRtDiff = self.maxRTDiffSpinBox.value()
        minMzRatio = self.minMZRatioSpinBox.value()

        peaksFile = self.rawPeakLineEdit.text()
        outputFile = self.outputLocationLineEdit.text()
        condensedFile = self.condensedOutputLineEdit.text()

        print("Running with config:")
        print("MinMz: {}\nmaxRtDiff: {}\nminMzRatio: {}\npeaksFile: {}\noutputFile: {}\ncondensedFile: {}".format(
            minMz, maxRtDiff, minMzRatio, peaksFile, outputFile, condensedFile))
        print("Parse!!")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(625, 382)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.gridGroupBox.setObjectName("gridGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.gridGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        
        
        self.rawPeakBtn = QtWidgets.QPushButton(self.gridGroupBox)
        self.rawPeakBtn.setObjectName("rawPeakBtn")
        #rawPeakBtn click
        self.rawPeakBtn.clicked.connect(self.raw_peak_btn_clicked)

        self.gridLayout.addWidget(self.rawPeakBtn, 3, 3, 1, 1)

        self.minMZRatioLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.minMZRatioLabel.setObjectName("minMZRatioLabel")
        self.gridLayout.addWidget(self.minMZRatioLabel, 1, 0, 1, 1)
        self.minMZLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.minMZLabel.setObjectName("minMZLabel")
        self.gridLayout.addWidget(self.minMZLabel, 0, 0, 1, 1)
        self.outputLocationLineEdit = QtWidgets.QLineEdit(self.gridGroupBox)
        self.outputLocationLineEdit.setReadOnly(True)
        self.outputLocationLineEdit.setObjectName("outputLocationLineEdit")
        self.gridLayout.addWidget(self.outputLocationLineEdit, 4, 2, 1, 1)
        self.maxRTDiffLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.maxRTDiffLabel.setObjectName("maxRTDiffLabel")
        self.gridLayout.addWidget(self.maxRTDiffLabel, 2, 0, 1, 1)
              
        self.condensedOutputBtn = QtWidgets.QPushButton(self.gridGroupBox)
        self.condensedOutputBtn.setObjectName("condensedOutputBtn")
        self.condensedOutputBtn.clicked.connect(self.condensed_btn_clicked)
        
        self.gridLayout.addWidget(self.condensedOutputBtn, 5, 3, 1, 1)
        
        self.condensedOutputLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.condensedOutputLabel.setObjectName("condensedOutputLabel")
        self.gridLayout.addWidget(self.condensedOutputLabel, 5, 0, 1, 1)
        self.condensedOutputLineEdit = QtWidgets.QLineEdit(self.gridGroupBox)
        self.condensedOutputLineEdit.setReadOnly(True)
        self.condensedOutputLineEdit.setObjectName("condensedOutputLineEdit")
        self.gridLayout.addWidget(self.condensedOutputLineEdit, 5, 2, 1, 1)
        
        self.outputCSVLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.outputCSVLabel.setObjectName("outputCSVLabel")
        self.gridLayout.addWidget(self.outputCSVLabel, 4, 0, 1, 1)
    
        self.rawPeakCSVLabel = QtWidgets.QLabel(self.gridGroupBox)
        self.rawPeakCSVLabel.setObjectName("rawPeakCSVLabel")
        self.gridLayout.addWidget(self.rawPeakCSVLabel, 3, 0, 1, 1)
        
        self.rawPeakLineEdit = QtWidgets.QLineEdit(self.gridGroupBox)
        self.rawPeakLineEdit.setEnabled(True)
        self.rawPeakLineEdit.setReadOnly(True)
        self.rawPeakLineEdit.setObjectName("rawPeakLineEdit")
        self.gridLayout.addWidget(self.rawPeakLineEdit, 3, 2, 1, 1)
        
        self.maxRTDiffSpinBox = QtWidgets.QDoubleSpinBox(self.gridGroupBox)
        self.maxRTDiffSpinBox.setMaximum(20.0)
        self.maxRTDiffSpinBox.setSingleStep(0.1)
        self.maxRTDiffSpinBox.setProperty("value", 2.0)
        self.maxRTDiffSpinBox.setObjectName("maxRTDiffSpinBox")
        self.gridLayout.addWidget(self.maxRTDiffSpinBox, 2, 2, 1, 1)
        
        self.parseBtn = QtWidgets.QPushButton(self.gridGroupBox)
        self.parseBtn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.parseBtn.clicked.connect(self.parse_btn_clicked)        
        self.parseBtn.setObjectName("parseBtn")


        self.gridLayout.addWidget(self.parseBtn, 6, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.minMZRatioSpinBox = QtWidgets.QDoubleSpinBox(self.gridGroupBox)
        self.minMZRatioSpinBox.setMaximum(1.0)
        self.minMZRatioSpinBox.setSingleStep(0.01)
        self.minMZRatioSpinBox.setProperty("value", 0.5)
        self.minMZRatioSpinBox.setObjectName("minMZRatioSpinBox")
        self.gridLayout.addWidget(self.minMZRatioSpinBox, 1, 2, 1, 1)

        self.outputLocationBtn = QtWidgets.QPushButton(self.gridGroupBox)
        self.outputLocationBtn.setObjectName("outputLocationBtn")
        self.outputLocationBtn.clicked.connect(self.output_loc_clicked)        
        self.gridLayout.addWidget(self.outputLocationBtn, 4, 3, 1, 1)

        self.minMZSpinBox = QtWidgets.QSpinBox(self.gridGroupBox)
        self.minMZSpinBox.setMaximum(1000000)
        self.minMZSpinBox.setSingleStep(10000)
        self.minMZSpinBox.setProperty("value", 50000)
        self.minMZSpinBox.setObjectName("minMZSpinBox")
        self.gridLayout.addWidget(self.minMZSpinBox, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.gridGroupBox, 3, 1, 1, 1)

        #uncomment for leo image in main window
        # img = QtGui.QImage(self.ICON)
        # self.mainTitleLabel = QtWidgets.QLabel(self.centralwidget)
        # self.mainTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.mainTitleLabel.setPixmap(QtGui.QPixmap.fromImage(img))
        # self.gridLayout_2.addWidget(self.mainTitleLabel, 0, 1, 1, 1)

        self.leoTitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.leoTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.leoTitleLabel.setFont(font)
        self.leoTitleLabel.setObjectName("leoTitleLabel")
        self.gridLayout_2.addWidget(self.leoTitleLabel, 1, 1, 1, 1)

        #main title lines
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 2, 1, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout_2.addWidget(self.line_3, 0, 1, 1, 1)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 625, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LEO"))
        self.rawPeakBtn.setText(_translate("MainWindow", "Pick Location"))
        self.minMZRatioLabel.setText(_translate("MainWindow", "Min MZ Ratio"))
        self.minMZLabel.setText(_translate("MainWindow", "Min MZ"))
        self.maxRTDiffLabel.setText(_translate("MainWindow", "Max RT Diff"))
        self.condensedOutputBtn.setText(_translate("MainWindow", "Pick Location"))
        self.condensedOutputLabel.setText(_translate("MainWindow", "Condensed Output CSV"))
        self.outputCSVLabel.setText(_translate("MainWindow", "Output CSV"))
        self.rawPeakCSVLabel.setText(_translate("MainWindow", "Raw Peak CSV"))
        self.maxRTDiffSpinBox.setToolTip(_translate("MainWindow", "Max difference from expeceted retention time."))
        self.parseBtn.setText(_translate("MainWindow", "Parse"))
        self.minMZRatioSpinBox.setToolTip(_translate("MainWindow", "Minimum ratio difference between test times."))
        self.outputLocationBtn.setText(_translate("MainWindow", "Pick Location"))
        self.minMZSpinBox.setToolTip(_translate("MainWindow", "Minimum intensity/"))
        #self.mainTitleLabel.setText(_translate("MainWindow", "Leo"))
        self.leoTitleLabel.setText(_translate("MainWindow", "Leo"))
