"""
Main Window controller
"""
import os
from PyQt5 import QtWidgets, uic, QtCore
import sys
import logging
import json
from PyQt5.QtCore import QAbstractTableModel, Qt, QSize
from PyQt5.QtGui import QBrush, QColor, QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QCheckBox, QTableWidget, QPushButton
from .program import NoteBook, Note, FILENAME_EXTENSION
from ipnotebook import confpars


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
            self.def_table_notes_setall(_notebook.notes)
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
            self.def_table_notes_setall(_notebook.notes)
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
        for i in range(len(marks_list)):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Checked)
            chkBoxItem.setText(marks_list[i])
            self.tableWidget_marks.setItem(i, 0, chkBoxItem)

    def def_table_notes_setall(self, notes):
        self.tableWidget_notes.setRowCount(len(notes))
        for i in range(len(notes)):
            iteam_ip = QTableWidgetItem(str(notes[i].ip_address))
            iteam_ip.setFlags(Qt.ItemIsEditable)
            iteam_ip.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 0, iteam_ip)
            iteam_mask = QTableWidgetItem(str(notes[i].mask))
            iteam_mask.setFlags(Qt.ItemIsEditable)
            iteam_mask.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 1, iteam_mask)
            iteam_date = QTableWidgetItem(str(notes[i].date_of_creation))
            iteam_date.setFlags(Qt.ItemIsEditable)
            iteam_date.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 2, iteam_date)
            marks_str = ''
            for mark in notes[i].marks:
                marks_str += ' ' + mark
            iteam_marks = QTableWidgetItem(marks_str)
            self.tableWidget_notes.setItem(i, 3, iteam_marks)
            iteam_text = QTableWidgetItem(str(notes[i].text))
            self.tableWidget_notes.setItem(i, 4, iteam_text)
            iteam_button = QPushButton(self.tableWidget_notes)
            iteam_button.setMaximumWidth(64)
            iteam_button.setMaximumHeight(24)
            iteam_button.setText('remove')
            self.tableWidget_notes.setCellWidget(i, 5, iteam_button)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.setColumnWidth(5,64)

    def def_table_notes_resize(self, event):
        if event.oldSize().width() != -1:
            self.tableWidget_notes.setColumnWidth(4, self.tableWidget_notes.columnWidth(4) + (event.size()-event.oldSize()).width())

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(confpars['main']['proj_root'], 'resources', 'mainwindow.ui'), self)

        self.statusBar.showMessage('Ready')
        self.action_saveas.triggered.connect(self.def_saveas)
        self.action_save.triggered.connect(self.def_save)
        self.action_open.triggered.connect(self.def_open)
        self.action_create.triggered.connect(self.def_create)
        self.action_exit.triggered.connect(self.def_exit)
        self.def_table_marks_clear()
        self.def_table_notes_clear()
        self.tableWidget_notes.resizeEvent = self.def_table_notes_resize

        self.show()

