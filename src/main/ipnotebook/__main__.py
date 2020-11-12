"""
Run program
"""

import sys
from PyQt5 import QtWidgets
from .mainwindow import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName("IP Notebook")
    app.setApplicationName("IP Notebook")
    mainWindow = MainWindow()
    app.exec_()


run()
