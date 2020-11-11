"""
Run program
"""

import sys
from PyQt5 import QtWidgets
from .mainwindow import MainWindow
import logging


FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)


def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName("IP Notebook")
    app.setApplicationName("IP Notebook")
    mainWindow = MainWindow()
    app.exec_()


run()
