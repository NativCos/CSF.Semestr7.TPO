"""
Main Window controller
"""
import os
from datetime import datetime
from ipaddress import IPv4Address
from PyQt5 import QtWidgets, uic, QtCore
import logging
import json
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QBrush, QColor, QKeySequence
from PyQt5.QtWidgets import QFileDialog, QDialog, QTableWidgetItem, QPushButton, QTableWidget, QShortcut
from .program import NoteBook, Note
from . import configs
from . import data_validation

_logger = logging.getLogger("ipnotebook.mainwindow")
_logger.setLevel(logging.DEBUG)


class MainWindow(QtWidgets.QMainWindow):
    _notebook = NoteBook()
    _path_to_work_notebook = ''
    _there_are_changes = False
    _refreshing_table_notes = False
    _refreshing_table_marks = False
    _exclusion_marks = set()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(configs['main']['proj_root'], 'resources', 'mainwindow.ui'), self)

        self.statusBar.showMessage('Не открыт блокнот')
        self.tableWidget_notes.cellChanged.connect(self.def_cellchanged)
        self.tableWidget_marks.itemClicked.connect(self.def_table_marks_changed)
        self.make_active_input(False)
        self.action_saveas.setEnabled(False)
        self.action_save.setEnabled(False)
        self.action_saveas.triggered.connect(self.def_saveas)
        self.action_save.triggered.connect(self.def_save)
        self.action_open.triggered.connect(self.def_open)
        self.action_create.triggered.connect(self.def_create)
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.pushButton_add.clicked.connect(self.def_addnote)
        self.pushButton_clearsearchstring.clicked.connect(self.def_clearsearchstring)
        self.pushButton_startsearchstring.clicked.connect(self.def_startsearch)
        self.def_table_marks_clear()
        self.def_table_notes_clear()
        self.tableWidget_notes.setSortingEnabled(True)  # TODO: как реализовать сортировку для столбйа дата???
        self.tableWidget_marks.setSortingEnabled(True)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.autosave)

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self._save_file)
        shortcut.activated.connect(lambda: self.statusBar.showMessage('Сохранено'))

        self._exclusion_marks = set()

        self.show()

    # TODO: проверка на заблокированный файл
    # TODO: проверка на не корректно подсунотый файл
    def _open_file(self):
        _logger.debug('call _open')
        with open(self._path_to_work_notebook, 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)
        self._notebook.changeEvent.connect(self.def_refresh_tables)
        self._notebook.changeEvent.connect(lambda: self.statusBar.showMessage('Есть несохраненные изменения'))

    def _create_file(self):
        _logger.debug('call _create')
        self._notebook = NoteBook()
        self._notebook.changeEvent.connect(self.def_refresh_tables)
        self._notebook.changeEvent.connect(lambda: self.statusBar.showMessage('Есть несохраненные изменения'))
        self._save_file()

    def _save_file(self):
        _logger.debug('call _save')
        with open(self._path_to_work_notebook, 'w') as f:
            json.dump(self._notebook.to_json(), fp=f)

    def autosave(self):
        self._save_file()
        self.autosave_timer.start(60 * 1000)
        self.statusBar.showMessage('Сохранено')

    def def_saveas(self):
        _logger.debug("call def_saveas!")
        dialog = QFileDialog(self, 'Сохранить как файл блокнота')
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['IP notebook (*.' + configs['main']['filename_extension'] + ')'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            self._path_to_work_notebook = dialog.selectedFiles()[0]
            self._save_file()
            self.setWindowTitle(self._path_to_work_notebook)
            self.autosave_timer.start(60 * 1000)
            self.statusBar.showMessage('Сохранено')

    def def_save(self):
        _logger.debug('call def_save')
        self._save_file()
        _logger.info("сохранение блокнота " + self._path_to_work_notebook)
        self.statusBar.showMessage('Сохранено')

    def def_create(self):
        _logger.debug("call def_create!")
        dialog = QFileDialog(self, 'Создать файл блокнота')
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['IP notebook (*.' + configs['main']['filename_extension'] + ')'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            if dialog.selectedFiles()[0][-5:] == '.' + configs['main']['filename_extension']:
                self._path_to_work_notebook = dialog.selectedFiles()[0]
            else:
                self._path_to_work_notebook = dialog.selectedFiles()[0] + '.' + configs['main']['filename_extension']
            self._create_file()
            self.def_refresh_tables()
            self.make_active_input(True)
            self.setWindowTitle(self._path_to_work_notebook)
            self.autosave_timer.start(60 * 1000)
            self.statusBar.showMessage('Сохранено')

    def def_open(self):
        _logger.debug("call def_open!")
        dialog = QFileDialog(self, 'Открыть файл блокнота')
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['IP notebook (*.' + configs['main']['filename_extension'] + ')'])
        if dialog.exec_() == QDialog.Accepted:
            _logger.debug('selected is ' + dialog.selectedFiles()[0])
            self._path_to_work_notebook = dialog.selectedFiles()[0]
            self._open_file()
            self.def_refresh_tables()
            self.make_active_input(True)
            self.setWindowTitle(self._path_to_work_notebook)
            self.autosave_timer.start(60 * 1000)
            self.statusBar.showMessage('Сохранено')

    def def_table_marks_clear(self):
        self.tableWidget_marks.setRowCount(0)

    def def_table_notes_clear(self):
        self.tableWidget_notes.setRowCount(0)

    def def_table_marks_set(self, marks_set, uncheck_this=None):
        self._refreshing_table_marks = True
        marks_list = list(marks_set)
        self.tableWidget_marks.setRowCount(len(marks_list))
        for i in range(len(marks_list)):
            chk_box_item = QTableWidgetItem()
            chk_box_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            try:
                if uncheck_this is not None and len(uncheck_this) != 0 and uncheck_this.index(marks_list[i]) >= 0:
                    chk_box_item.setCheckState(Qt.Unchecked)
                else:
                    chk_box_item.setCheckState(Qt.Checked)
            except ValueError:
                chk_box_item.setCheckState(Qt.Checked)
            chk_box_item.setText(marks_list[i])
            self.tableWidget_marks.setItem(i, 0, chk_box_item)
        self._refreshing_table_marks = False

    def def_table_notes_set(self, notes):
        self._refreshing_table_notes = True
        self.tableWidget_notes.setRowCount(len(notes))
        for i in range(len(notes)):
            item_ip = QTableWidgetItem(str(notes[i].ip_address))
            item_ip.setFlags(Qt.ItemIsEditable)
            item_ip.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 0, item_ip)
            item_mask = QTableWidgetItem(str(notes[i].mask))
            item_mask.setFlags(Qt.ItemIsEditable)
            item_mask.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 1, item_mask)
            item_date = QTableWidgetItem(notes[i].date_of_creation.strftime('%H:%M %d %B %Y'))
            item_date.setFlags(Qt.ItemIsEditable)
            item_date.setForeground(QBrush(QColor(255, 255, 255)))
            self.tableWidget_notes.setItem(i, 2, item_date)
            item_marks = QTableWidgetItem(' '.join(notes[i].marks))
            self.tableWidget_notes.setItem(i, 3, item_marks)
            item_text = QTableWidgetItem(str(notes[i].text))
            self.tableWidget_notes.setItem(i, 4, item_text)
            item_button = QPushButton(self.tableWidget_notes)
            item_button.setMaximumWidth(64)
            item_button.setMaximumHeight(24)
            item_button.setText('remove')
            item_button.note_id = notes[i].ID
            item_button.clicked.connect(self.def_removenote)
            self.tableWidget_notes.setCellWidget(i, 5, item_button)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_notes.setColumnWidth(5, 64)
        self._refreshing_table_notes = False

    def def_table_marks_changed(self, item):
        if self._refreshing_table_marks:
            return
        if item.checkState() == QtCore.Qt.Unchecked:
            self._exclusion_marks.add(item.text())
        elif set([item.text()]).issubset(self._exclusion_marks):
            self._exclusion_marks.remove(item.text())
        self.def_table_notes_set(self._notebook.get_all_notes(exclusion_marks=self._exclusion_marks))

    def def_addnote(self):
        ip_str = self.add_plainTextEdit_ip.toPlainText()
        mask_str = self.add_plainTextEdit_mask.toPlainText()
        marks_str = self.add_plainTextEdit_marks.toPlainText()
        text_str = self.add_plainTextEdit_text.toPlainText()

        marks = marks_str.strip().split(' ')
        try:
            marks.remove('')
        except ValueError:
            pass
        if data_validation.is_valid_ipaddress(ip_str) and \
                data_validation.is_valid_mask(mask_str) and \
                data_validation.is_valid_marks(marks) and \
                data_validation.is_valid_text(text_str):
            self.statusBar.showMessage('Некорректные данные для добавления')

        n = Note(IPv4Address(ip_str), IPv4Address(mask_str), datetime.now(), text_str, set(marks))
        self._notebook.add_note(n)

        self.add_plainTextEdit_ip.setPlainText('')
        self.add_plainTextEdit_mask.setPlainText('')
        self.add_plainTextEdit_marks.setPlainText('')
        self.add_plainTextEdit_text.setPlainText('')

    def def_removenote(self):
        sender = self.sender()
        self._notebook.remove_note(sender.note_id)

    def def_startsearch(self):  # TODO: сделать поиск
        if self.lineEdit_search.text() != '':
            self.def_table_notes_set(self._notebook.full_text_search(self.lineEdit_search.text()))
        else:
            self.def_table_notes_clear()

    def def_clearsearchstring(self):
        self.lineEdit_search.setText('')
        self.def_refresh_tables()

    # TODO: TDD
    def def_cellchanged(self, r, c):
        if self._refreshing_table_notes:
            return
        n = self._notebook.get_note(self.tableWidget_notes.cellWidget(r, 5).note_id)
        n.marks = set(self.tableWidget_notes.item(r, 3).text().strip().split(' '))  # TODO: нет проверки фходного значения
        if len(n.marks) == 1 and '' in n.marks:
            n.marks = set()
        n.text = self.tableWidget_notes.item(r, 4).text()  # TODO: не проверки входного значения
        self.def_refresh_tables()
        self.statusBar.showMessage('Есть несохраненные изменения')

    def def_refresh_tables(self):
        self.def_table_notes_set(self._notebook.get_all_notes(exclusion_marks=self._exclusion_marks))

        uncheck_this = []
        for row in range(self.tableWidget_marks.rowCount()):
            if self.tableWidget_marks.item(row, 0).checkState() == QtCore.Qt.Unchecked:
                uncheck_this.append(self.tableWidget_marks.item(row, 0).text())
        self.def_table_marks_set(self._notebook.get_all_marks(), uncheck_this=uncheck_this)

        self._exclusion_marks = set()
        for row in range(self.tableWidget_marks.rowCount()):
            if self.tableWidget_marks.item(row, 0).checkState() == QtCore.Qt.Unchecked:
                self._exclusion_marks.add(self.tableWidget_marks.item(row, 0).text())

    def make_active_input(self, active: bool):
        self.add_plainTextEdit_ip.setVisible(active)
        self.add_plainTextEdit_mask.setVisible(active)
        self.add_plainTextEdit_marks.setVisible(active)
        self.add_plainTextEdit_text.setVisible(active)
        self.pushButton_add.setVisible(active)

        self.lineEdit_search.setVisible(active)
        self.pushButton_startsearchstring.setVisible(active)
        self.pushButton_clearsearchstring.setVisible(active)

        self.action_saveas.setEnabled(True)
        self.action_save.setEnabled(True)
