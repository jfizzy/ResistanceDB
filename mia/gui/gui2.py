# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mia.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import datetime
from time import time

from mia_backend.config import Config
from mia_backend.mia_manager import MiaManager

class Ui_MainWindow(object):
    def __init__(self, parent):
        self.systemTray = QtWidgets.QSystemTrayIcon()
        self.parent = parent

        systrayMenu = QtWidgets.QMenu()
        openAction = systrayMenu.addAction("open")
        openAction.triggered.connect(self.systray_open)

        closeAction = systrayMenu.addAction("close")
        closeAction.triggered.connect(self.systray_close)

        self.systemTray.setIcon(QtGui.QIcon("gui/mia.gif"))
        #self.systemTrayIcon.setVisible(True)

        self.systemTray.setToolTip("mia")
        self.systemTray.activated.connect(self.systray_clicked)

        self.systemTray.setContextMenu(systrayMenu)
        self.systemTray.show()

    def loaded(self):
        self._manager = MiaManager(self)
        self.update_config(self._manager.get_config())

    def shutdown(self):
        self._manager.shutdown()
        self.systemTray.hide()

    def update_config(self, config):
        """
            updates UI config values based on values of a Config object
        """
        # remember to enable, insert, then disable the field - user shouldnt be allowed to update field
        if config.INTERIM:
            self.interimDirectoryField.setText(config.INTERIM.replace("/","\\"))
        
        if config.DST_DIR:
            self.destinationDirectoryField.setText(config.DST_DIR.replace("/","\\"))

        if config.CONVERTER:
            self.readwLocField.setText(config.CONVERTER.replace("/","\\"))

        if config.INTERVAL:
            self.intervalSlider.setSliderPosition(config.INTERVAL)
        
        if config.DATABASE:
            self.databaseField.setText(config.DATABASE.replace("/","\\"))

        if config.SRC_DIRS:
            for src in config.SRC_DIRS:
                item = QtWidgets.QListWidgetItem(src.replace("/","\\"))
                self.srcListView.addItem(item)


    def collect_config(self, config):
        """
            collects config variables from the GUI and sets
            them to the passed in config class
        """
        dst = self.destinationDirectoryField.text()
        interim = self.interimDirectoryField.text()
        exe = self.readwLocField.text()
        database = self.databaseField.text()

        srcs = []

        for index in range(self.srcListView.count()):
            srcs.append(self.srcListView.item(index).text())

        interval = self.intervalSlider.value()
        ext = 'raw'
        flags = "--compress --mzXML"

        config.set_config(srcs, dst, exe, flags, interim, ext, interval, database)

    def systray_clicked(self, event):
        """ user clicked on system tray icon, ensure it wasn't a context menu click, otherwise show """
        if event != QtWidgets.QSystemTrayIcon.Context:
            self.parent.show()

    def systray_open(self):
        """ User clicked 'Open' on system tray, show window """
        self.parent.show()

    def systray_close(self):
        #self.parent.shut_er_down()
        msg = "Are you sure you want to quit Mia?\n"
        msg += "All file conversion will be halted."
        reply = QtWidgets.QMessageBox.question(self.parent,
                    'Quit?',
                    msg, QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            self.shutdown()
            self.parent.shut_er_down()

    def add_src_btn_clicked(self):
        """ """
        dir_name = QtWidgets.QFileDialog.getExistingDirectory()
        
        if dir_name:
            dir_name = dir_name.replace("/","\\")
            for index in range(self.srcListView.count()):
                if self.srcListView.item(index).text() == dir_name:
                    self.update_status("Directory already in sources.")
                    return

            item = QtWidgets.QListWidgetItem(dir_name)
            self.srcListView.addItem(item)

    def update_status(self, msg):
        msg = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S - ') + msg
        item = QtWidgets.QListWidgetItem(msg)
        self.statusList.insertItem(0, item)

    def del_src_btn_clicked(self):
        """ """
        items = self.srcListView.selectedItems()
        for item in items:
            self.srcListView.takeItem(self.srcListView.row(item))

    def add_interim_btn_clicked(self):
        """ """
        dir_name = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_name:
            self.interimDirectoryField.setText(dir_name.replace("/","\\"))

    def readw_loc_btn_clicked(self):
        """ """
        file_name = QtWidgets.QFileDialog.getOpenFileName()
        if file_name:
           self.readwLocField.setText(file_name[0].replace("/","\\"))

    def add_dst_btn_clicked(self):
        """ """
        dir_name = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_name:
            self.destinationDirectoryField.setText(dir_name.replace("/","\\"))

    def database_btn_clicked(self):
        """ """
        dlg = QtWidgets.QFileDialog(self.parent)
        dlg.setNameFilters(["Sqlite3 Database Files (*.db)"])
        dlg.selectNameFilter("Sqlite3 Database Files (*.db)")
        
        dlg.exec_()
        files = dlg.selectedFiles()
        if files:
            self.databaseField.setText(files[0].replace("/","\\"))

    def interval_slider_changed(self):
        """ """
        self.intervalLbl.setText("Interval (minutes):    {}".format(self.intervalSlider.value()))

    def mia_start_btn_clicked(self):
        """ """
        config = Config(None)
        self.collect_config(config)
        self._manager.start(config, self.mia_starting)

    def mia_starting(self):
        """ handles if any code is desired to run after mia initializes """
        self.startMiaBtn.setEnabled(False)
        self.stopMiaBtn.setEnabled(True)
        self.restartMiaBtn.setEnabled(True)

    def mia_reset_btn_clicked(self):
        """ """
        print("reset")

    def mia_stop_btn_clicked(self):
        """ """
        self._manager.stop(self.mia_stopped)

    def mia_stopped(self):
        """ callback for mia backend
            place code here if we want to run code when
            mia stops transferring
        """
        self.startMiaBtn.setEnabled(True)
        self.stopMiaBtn.setEnabled(False)
        self.restartMiaBtn.setEnabled(False)

    def mia_shutdown_btn_clicked(self):
        """ """
        print("shutdown")

    def interval_changed(self):
        """ """
        if self.parallelCheckBox.isChecked():
            print("Checked!")
        else:
            print("Unchecked!")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(709, 585)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_2.addWidget(self.line_2, 0, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.removeSrcBtn = QtWidgets.QPushButton(self.groupBox)
        self.removeSrcBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.removeSrcBtn.setObjectName("removeSrcBtn")
        self.gridLayout.addWidget(self.removeSrcBtn, 1, 3, 1, 1)
        self.removeSrcBtn.clicked.connect(self.del_src_btn_clicked)

        self.interimDirectoryField = QtWidgets.QLineEdit(self.groupBox)
        self.interimDirectoryField.setEnabled(True)
        self.interimDirectoryField.setMinimumSize(QtCore.QSize(0, 25))
        self.interimDirectoryField.setReadOnly(True)
        self.interimDirectoryField.setObjectName("interimDirectoryField")
        self.gridLayout.addWidget(self.interimDirectoryField, 2, 0, 1, 3)

        self.destinationDirectoryField = QtWidgets.QLineEdit(self.groupBox)
        self.destinationDirectoryField.setMinimumSize(QtCore.QSize(0, 25))
        self.destinationDirectoryField.setReadOnly(True)
        self.destinationDirectoryField.setObjectName("destinationDirectoryField")
        self.gridLayout.addWidget(self.destinationDirectoryField, 3, 0, 1, 3)

        self.addInterimBtn = QtWidgets.QPushButton(self.groupBox)
        self.addInterimBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.addInterimBtn.setObjectName("addInterimBtn")
        self.gridLayout.addWidget(self.addInterimBtn, 2, 3, 1, 1)
        self.addInterimBtn.clicked.connect(self.add_interim_btn_clicked)

        self.statusList = QtWidgets.QListWidget(self.groupBox)
        self.statusList.setObjectName("statusList")
        self.gridLayout.addWidget(self.statusList, 8, 0, 1, 4)

        #QListView
        self.srcListView = QtWidgets.QListWidget(self.groupBox)
        self.srcListView.setObjectName("srcListView")
        self.gridLayout.addWidget(self.srcListView, 0, 0, 2, 3)

        self.readwLocField = QtWidgets.QLineEdit(self.groupBox)
        self.readwLocField.setMinimumSize(QtCore.QSize(0, 25))
        self.readwLocField.setReadOnly(True)
        self.readwLocField.setObjectName("readwLocField")
        self.gridLayout.addWidget(self.readwLocField, 4, 0, 1, 3)
        self.intervalLbl = QtWidgets.QLabel(self.groupBox)
        self.intervalLbl.setObjectName("intervalLbl")
        self.gridLayout.addWidget(self.intervalLbl, 6, 0, 1, 1)

        self.addDstBtn = QtWidgets.QPushButton(self.groupBox)
        self.addDstBtn.setObjectName("addDstBtn")
        self.gridLayout.addWidget(self.addDstBtn, 3, 3, 1, 1)
        self.addDstBtn.clicked.connect(self.add_dst_btn_clicked)

        self.readwLocBtn = QtWidgets.QPushButton(self.groupBox)
        self.readwLocBtn.setObjectName("readwLocBtn")
        self.gridLayout.addWidget(self.readwLocBtn, 4, 3, 1, 1)
        self.readwLocBtn.clicked.connect(self.readw_loc_btn_clicked)


        ###TEST
        self.databaseField = QtWidgets.QLineEdit(self.groupBox)
        self.databaseField.setMinimumSize(QtCore.QSize(0, 25))
        self.databaseField.setReadOnly(True)
        self.databaseField.setObjectName("databaseField")
        self.gridLayout.addWidget(self.databaseField, 5, 0, 1, 3)

        self.databaseBtn = QtWidgets.QPushButton(self.groupBox)
        self.databaseBtn.setObjectName("databaseBtn")
        self.gridLayout.addWidget(self.databaseBtn, 5, 3, 1, 1)

        ##fix this
        self.databaseBtn.clicked.connect(self.database_btn_clicked)

        ###END TEST

        self.intervalSlider = QtWidgets.QSlider(self.groupBox)
        self.intervalSlider.setMinimum(5)
        self.intervalSlider.setSliderPosition(25)
        self.intervalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.intervalSlider.setObjectName("intervalSlider")
        self.intervalSlider.valueChanged.connect(self.interval_slider_changed)

        self.gridLayout.addWidget(self.intervalSlider, 6, 1, 1, 2)
        self.addSrcBtn = QtWidgets.QPushButton(self.groupBox)
        self.addSrcBtn.setMinimumSize(QtCore.QSize(0, 25))
        self.addSrcBtn.setObjectName("addSrcBtn")
        self.addSrcBtn.clicked.connect(self.add_src_btn_clicked)
        self.gridLayout.addWidget(self.addSrcBtn, 0, 3, 1, 1)

        self.parallelCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.parallelCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.parallelCheckBox.setStyleSheet("spacing: 80%;")
        self.parallelCheckBox.setObjectName("parallelCheckBox")
        self.parallelCheckBox.stateChanged.connect(self.interval_changed)
        self.gridLayout.addWidget(self.parallelCheckBox, 6, 3, 1, 1)
        
        #self.statusLbl = QtWidgets.QLabel(self.groupBox)
        #self.statusLbl.setObjectName("statusLbl")
        #self.gridLayout.addWidget(self.statusLbl, 8, 0, 1, 1)

        self.startMiaBtn = QtWidgets.QPushButton(self.groupBox)
        self.startMiaBtn.setObjectName("startMiaBtn")
        self.startMiaBtn.clicked.connect(self.mia_start_btn_clicked)
        self.gridLayout.addWidget(self.startMiaBtn, 7, 0, 1, 1)

        self.stopMiaBtn = QtWidgets.QPushButton(self.groupBox)
        self.stopMiaBtn.setObjectName("stopMiaBtn")
        self.gridLayout.addWidget(self.stopMiaBtn, 7, 1, 1, 1)
        self.stopMiaBtn.setEnabled(False)
        self.stopMiaBtn.clicked.connect(self.mia_stop_btn_clicked)

        self.restartMiaBtn = QtWidgets.QPushButton(self.groupBox)
        self.restartMiaBtn.setObjectName("restartMiaBtn")
        self.gridLayout.addWidget(self.restartMiaBtn, 7, 2, 1, 1)
        self.restartMiaBtn.setEnabled(False)
        self.restartMiaBtn.clicked.connect(self.mia_reset_btn_clicked)

        self.shtDownBtn = QtWidgets.QPushButton(self.groupBox)
        self.shtDownBtn.setObjectName("shtDownBtn")
        self.gridLayout.addWidget(self.shtDownBtn, 7, 3, 1, 1)
        self.shtDownBtn.clicked.connect(self.mia_shutdown_btn_clicked)

        self.srcListView.raise_()
        self.addSrcBtn.raise_()
        self.removeSrcBtn.raise_()
        self.interimDirectoryField.raise_()
        self.destinationDirectoryField.raise_()
        self.addInterimBtn.raise_()
        self.addDstBtn.raise_()
        self.readwLocField.raise_()
        self.readwLocBtn.raise_()

        ##test
        self.databaseBtn.raise_()
        ##test

        self.parallelCheckBox.raise_()
        self.intervalSlider.raise_()
        self.intervalLbl.raise_()
        self.statusList.raise_()
        self.startMiaBtn.raise_()
        self.statusList.raise_()
        #self.statusLbl.raise_()
        self.stopMiaBtn.raise_()
        self.restartMiaBtn.raise_()
        self.shtDownBtn.raise_()
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 709, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mia!"))
        self.label.setText(_translate("MainWindow", "Mia"))
        self.groupBox.setTitle(_translate("MainWindow", "Config"))
        self.removeSrcBtn.setText(_translate("MainWindow", "Remove Source"))
        self.interimDirectoryField.setToolTip(_translate("MainWindow", "<html><head/><body><p>This is the location where the files will be copied for temporary storage before they are converted to mzXML files. For speed purposes, it is recommended that a location on the device that Mia is running on is used. These files will be deleted after they have served their purposes.</p></body></html>"))
        self.interimDirectoryField.setPlaceholderText(_translate("MainWindow", "Interim Folder"))
        self.destinationDirectoryField.setToolTip(_translate("MainWindow", "<html><head/><body><p>This is the final root destination for the converted files. The files will retain their directory structure from the source directories and use this folder as the location to store the copied directory structure.</p></body></html>"))
        self.destinationDirectoryField.setPlaceholderText(_translate("MainWindow", "Destination Directory"))
        self.addInterimBtn.setText(_translate("MainWindow", "Choose Copy Location"))
        self.readwLocField.setPlaceholderText(_translate("MainWindow", "ReAdW.exe Location"))
        self.intervalLbl.setText(_translate("MainWindow", "Interval(minutes):    {}".format(self.intervalSlider.value())))
        self.addDstBtn.setText(_translate("MainWindow", "Choose Destination"))
        self.readwLocBtn.setText(_translate("MainWindow", "Choose ReAdW Loc"))
        #test
        self.databaseField.setPlaceholderText(_translate("MainWindow", "Datbase Location"))     
        self.databaseBtn.setText(_translate("MainWindow", "Database Location"))
        self.databaseField.setToolTip(_translate("MainWindow", "<html><head/><body><p>The location of the sqlite3 database file to store moved files.</p></body></html>"))        
        ##
        self.addSrcBtn.setText(_translate("MainWindow", "Add Source"))
        self.parallelCheckBox.setToolTip(_translate("MainWindow", "<html><head/><body><p>To be implemented</p></body></html>"))
        self.parallelCheckBox.setText(_translate("MainWindow", "Paralellize"))
        #self.statusLbl.setText(_translate("MainWindow", "Status"))
        self.startMiaBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Start Mia with current configurations.</p></body></html>"))
        self.startMiaBtn.setText(_translate("MainWindow", "Start Mia"))
        self.stopMiaBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Stop Mia. Mia will first finish the last most conversion to ensure no duplicate files. This could take a couple minutes to finish, depending on the size of the raw file.</p></body></html>"))
        self.stopMiaBtn.setText(_translate("MainWindow", "Stop Mia"))
        self.restartMiaBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Restart Mia with selected new configurations.</p></body></html>"))
        self.restartMiaBtn.setText(_translate("MainWindow", "Restart Mia"))
        self.shtDownBtn.setToolTip(_translate("MainWindow", "<html><head/><body><p>Stop Mia and quit the Mia application.</p></body></html>"))
        self.shtDownBtn.setText(_translate("MainWindow", "Shut Down"))

