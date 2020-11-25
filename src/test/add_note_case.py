import unittest
import time
import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from threading import Thread

from PyQt5.QtWidgets import QTableWidgetItem

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
        time.sleep(2)
        self.myapp.mainWindow._path_to_work_notebook = os.path.join('resources', 'test.ntip')
        self.myapp.mainWindow._open_file()
        self.myapp.mainWindow.activate_window()

    def test_update(self):
        marks_set = {'ads', 'vsdb', 'c234', '345', 's'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self.myapp.mainWindow.update_note(note_id, marks_str, '')
        self.assertEqual(self.myapp.mainWindow._notebook.get_note(note_id).marks, marks_set)

        text = 'dfkuilg igdf 7g799794379349 I LSIUVILudgv v'
        note_id = 1
        self.myapp.mainWindow.update_note(note_id, '', text)
        self.assertEqual(self.myapp.mainWindow._notebook.get_note(note_id).text, text)

    def tearDown(self):
        QtCore.QCoreApplication.instance().quit()


if __name__ == '__main__':
    unittest.main()
