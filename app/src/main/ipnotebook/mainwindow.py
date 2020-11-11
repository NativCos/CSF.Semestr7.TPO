"""
Main Window controller
"""
from PyQt5 import QtWidgets, uic, QtCore
import sys
import logging

from PyQt5.QtWidgets import QInputDialog, QFileDialog

from .program import NoteBook, Note, FILENAME_EXTENSION


_logger = logging.getLogger("ipnotebook.mainwindow")
_logger.setLevel(logging.DEBUG)


notebook = NoteBook()


class MainWindow(QtWidgets.QMainWindow):
    def def_saveas(self):
        _logger.debug("call def_saveas!")
        notebook.notes.append(Note())
        notebook.save('test.'+FILENAME_EXTENSION)
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        dialog = QtGui.QFileDialog(self, 'Audio Files', directory, filter)
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.setSidebarUrls([QtCore.QUrl.fromLocalFile(place)])
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self._audio_file = dialog.selectedFiles()[0]

    def def_save(self):
        _logger.debug("call def_save!")

    def def_open(self):
        _logger.debug("call def_open!")
        notebook = NoteBook.open('test.'+FILENAME_EXTENSION)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('resources/mainwindow.ui', self)

        self.statusBar().showMessage('Ready')
        self.action_saveas.triggered.connect(self.def_saveas)
        self.action_save.triggered.connect(self.def_save)
        self.action_open.triggered.connect(self.def_open)
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        self.show()