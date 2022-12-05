# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modpack_installer.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import zipfile
import os
import shutil
import time
import requests

APPDATA = os.getenv('APPDATA')
MINECRAFT_FOLDER = os.path.join(APPDATA, '.minecraft')
MODS_FOLDER = os.path.join(APPDATA, '.minecraft', 'mods')
MODS_URL = 'https://github.com/Arthur-UBdx/mods_minecraft/zipball/main'
FABRIC_FOLDER = os.path.join(MINECRAFT_FOLDER, 'fabric_installers')
FABRIC_URL = 'https://github.com/Arthur-UBdx/fabric_minecraft/zipball/main'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Installateur magique de la raciscothèque")
        MainWindow.resize(511, 342)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 270, 471, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.install_fabric_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.install_fabric_button.setObjectName("install_fabric_button")
        self.horizontalLayout.addWidget(self.install_fabric_button)
        self.download_mods_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.download_mods_button.setObjectName("download_mods_button")
        self.horizontalLayout.addWidget(self.download_mods_button)
        self.delete_mods_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.delete_mods_button.setObjectName("delete_mods_button")
        self.horizontalLayout.addWidget(self.delete_mods_button)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 471, 211))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("kanye.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(26, 12, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(14)
        font.setItalic(False)
        font.setUnderline(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.install_fabric_button.clicked.connect(self.install_fabric)
        self.download_mods_button.clicked.connect(self.download_mods)
        self.delete_mods_button.clicked.connect(self.delete_mods)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Installateur magique de la raciscothèque"))
        self.install_fabric_button.setText(_translate("MainWindow", "Installer Fabric"))
        self.download_mods_button.setText(_translate("MainWindow", "Télécharger et installer les mods"))
        self.delete_mods_button.setText(_translate("MainWindow", "Supprimer les mods"))
        self.label.setText(_translate("MainWindow", "L\'installateur magique de la raciscothèque"))
        
    def _unzip_files(self,zip_path):
        folder = os.path.dirname(zip_path)
        for k in range(10):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(folder)
            folders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
            if folders: 
                for file in os.listdir(os.path.join(folder, folders[0])):
                    os.rename(os.path.join(folder, folders[0], file), os.path.join(folder, file))
                shutil.rmtree(os.path.join(folder, folders[0]))
                os.remove(zip_path)
                return 0
            else:
                continue
        else:
            return 1
        
    def install_fabric(self):
        try:
            shutil.rmtree(FABRIC_FOLDER)
        except FileNotFoundError:
            pass
        if not os.path.isdir(os.path.join(MINECRAFT_FOLDER, 'fabric_installers')):
            os.mkdir(os.path.join(MINECRAFT_FOLDER, 'fabric_installers'))
        
        r = requests.get(FABRIC_URL, allow_redirects=True)
        open(os.path.join(FABRIC_FOLDER, 'fabric.zip'), 'wb').write(r.content)
        while not os.path.isfile(os.path.join(FABRIC_FOLDER, 'fabric.zip')) or os.path.getsize(os.path.join(FABRIC_FOLDER, 'fabric.zip')) == 0:
            time.sleep(1)
        if self._unzip_files(os.path.join(FABRIC_FOLDER, 'fabric.zip')):
            raise Exception("Un zipping error")
            return -1
        for file in os.listdir(FABRIC_FOLDER):
            if file.endswith('.exe'):
                os.system(f'cd {FABRIC_FOLDER} && {file}')
                return 0
        else:
            raise FileNotFoundError('No .exe file found in fabric_installers folder.')
            return -1

    def download_mods(self):
        self.delete_mods(show_dialog=False)
        if not os.path.isdir(MODS_FOLDER):
            os.mkdir(MODS_FOLDER)
        r = requests.get(MODS_URL, allow_redirects=True)
        open(os.path.join(MODS_FOLDER, 'mods.zip'), 'wb').write(r.content)
        while not os.path.isfile(os.path.join(MODS_FOLDER, 'mods.zip')) or os.path.getsize(os.path.join(MODS_FOLDER, 'mods.zip')) == 0:
            time.sleep(1)
        if self._unzip_files(os.path.join(MODS_FOLDER, 'mods.zip')):
            return -1
        return 0

    def delete_mods(self, show_dialog=True):
        shutil.rmtree(MODS_FOLDER)
        os.mkdir(MODS_FOLDER)
        return 0
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())