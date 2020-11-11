"""
Main Window controller
"""
import os

from PyQt5 import QtWidgets, uic, QtCore
import sys
import logging
import json

from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QCheckBox, QTableWidget

from .program import NoteBook, Note, FILENAME_EXTENSION


_logger = logging.getLogger("ipnotebook.mainwindow")
_logger.setLevel(logging.DEBUG)


_notebook = NoteBook()
_path_to_work_notebook = ''
_there_are_changes = False


def _open():
    global _notebook
    with open(_path_to_work_notebook, 'r') as f:
        json_dict = json.load(fp=f)
    _notebook = NoteBook.fromJSON(json_dict)


def _save():
    global _notebook
    with open(_path_to_work_notebook, 'w') as f:
        json.dump(_notebook.toJSON(), fp=f)


def _create():
    global _notebook
    _notebook = NoteBook()
    _save()


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

    def def_create(self):
        global _path_to_work_notebook
        _logger.debug("call def_create!")
        dialog = QFileDialog(self, 'Создать файл блокнота')
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilters(['IP notebook (*.ntip)'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            if dialog.selectedFiles()[0][-5:] == '.'+FILENAME_EXTENSION:
                _path_to_work_notebook = dialog.selectedFiles()[0]
            else:
                _path_to_work_notebook = dialog.selectedFiles()[0] + '.' + FILENAME_EXTENSION
            _create()
            self.action_saveas.setEnabled(True)
            self.action_save.setEnabled(True)
            self.setWindowTitle(_path_to_work_notebook)

    def def_open(self):
        global _path_to_work_notebook
        _logger.debug("call def_open!")
        dialog = QFileDialog(self, 'Открыть файл блокнота')
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilters(['IP notebook (*.ntip)'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            _path_to_work_notebook = dialog.selectedFiles()[0]
            _open()
            self.action_saveas.setEnabled(True)
            self.action_save.setEnabled(True)
            self.setWindowTitle(_path_to_work_notebook)

    def def_exit(self):
        QtCore.QCoreApplication.instance().quit()

    def def_table_marks_clear(self):
        self.tableWidget_marks.setRowCount(0)

    def def_table_notes_clear(self):
        self.tableWidget_notes.setRowCount(0)

    def def_table_marks_setall(self, marks_list):
        for i in len(marks_list):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Checked)
            chkBoxItem.setText(marks_list[i])
            self.tableWidget_marks.setItem(i, 0, chkBoxItem)

    def def_table_notes_setall(self, notes):
        self.tableWidget_notes.setRowCount(len(notes))
        for i in len(notes):
            iteam_ip = QTableWidgetItem(str(notes[i].ip_address))
            self.tableWidget_notes.setItem(i, 0, iteam_ip)
            iteam_mask = QTableWidgetItem(str(notes[i].mask))
            self.tableWidget_notes.setItem(i, 1, iteam_mask)
            iteam_date = QTableWidgetItem(str(notes[i].date_of_creation))
            self.tableWidget_notes.setItem(i, 2, iteam_date)
            iteam_marks = QTableWidgetItem(str(notes[i].date_of_creation))
            iteam_marks.setFlags(Qt.ItemIsEditable)
            self.tableWidget_notes.setItem(i, 3, iteam_marks)
            iteam_marks = QTableWidgetItem(str(notes[i].date_of_creation))
            iteam_marks.setFlags(Qt.ItemIsEditable)
            self.tableWidget_notes.setItem(i, 3, iteam_marks)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'mainwindow.ui'), self)

        self.statusBar.showMessage('Ready')
        self.action_saveas.triggered.connect(self.def_saveas)
        self.action_save.triggered.connect(self.def_save)
        self.action_open.triggered.connect(self.def_open)
        self.action_create.triggered.connect(self.def_create)
        self.action_exit.triggered.connect(self.def_exit)
        self.def_table_marks_clear()
        self.def_table_notes_clear()
        self.tableWidget_notes = QTableWidget()
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.show()

