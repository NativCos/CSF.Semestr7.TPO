import unittest
import time
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from threading import Thread

from ipnotebook.mainwindow import MainWindow


class RunAppThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow()
        self.app.exec_()


class AddNoteCase(unittest.TestCase):
    def setUp(self) -> None:
        self.myapp = RunAppThread()
        self.myapp.start()
        time.sleep(5)

    def test_something(self):
        self.myapp.mainWindow.def_open()

    def tearDown(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == '__main__':
    unittest.main()
