"""
Main Window controller
"""
import os

from PyQt5 import QtWidgets, uic, QtCore
import sys
import logging
import json

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QCheckBox

from .program import NoteBook, Note, FILENAME_EXTENSION


_logger = logging.getLogger("ipnotebook.mainwindow")
_logger.setLevel(logging.DEBUG)


_notebook = NoteBook()
_path_to_work_notebook = ''


def _open():
    global _notebook
    with open(_path_to_work_notebook, 'r') as f:
        json_dict = json.load(fp=f)
    _notebook = NoteBook.fromJSON(json_dict)


def _save():
    global _notebook
    with open(_path_to_work_notebook, 'w') as f:
        json.dump(_notebook.toJSON(), fp=f)


class MainWindow(QtWidgets.QMainWindow):
    def def_saveas(self):
        _logger.debug("call def_saveas!")
        _notebook.notes.append(Note())
        dialog = QFileDialog(self, 'Сохранить как файл блокнота')
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilters(['IP notebook (*.ntip)'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            _save()

    def def_save(self):
        _logger.debug("call def_save!")
        _save()

    def def_open(self):
        _logger.debug("call def_open!")
        dialog = QFileDialog(self, 'Открыть файл блокнота')
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilters(['IP notebook (*.ntip)'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            _path_to_work_notebook = dialog.selectedFiles()[0]
            _open()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'mainwindow.ui'), self)

        self.statusBar.showMessage('Ready')
        self.action_saveas.triggered.connect(self.def_saveas)
        self.action_save.triggered.connect(self.def_save)
        self.action_open.triggered.connect(self.def_open)
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)

        self.show()


"""
        for i in range(3):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Unchecked)
            chkBoxItem.setText("test")
            self.tableWidget_marks.setItem(i, 0, chkBoxItem)
"""