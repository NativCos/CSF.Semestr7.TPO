"""
Business logic
"""
from datetime import datetime
from ipaddress import IPv4Address
from PyQt5.QtCore import pyqtSignal, QObject
import logging
from . import configs, data_validation

_logger = logging.getLogger("ipnotebook.program")
_logger.setLevel(logging.DEBUG)


class DataDontValidException(BaseException):
    """данные некорректны"""


class Note:
    """one note about ip address"""
    ID = -1
    ip_address = IPv4Address('0.0.0.0')
    mask = IPv4Address('0.0.0.0')
    date_of_creation = datetime.now()
    text = ""
    marks = set()

    def __init__(self, ip_address: IPv4Address = None, mask: IPv4Address = None, date_of_creation: datetime = None, text: str = None, marks: set = None):
        self.ip_address = ip_address
        self.mask = mask
        self.date_of_creation = date_of_creation
        self.text = text
        self.marks = marks

    def to_json(self):
        return {'ip_address': str(self.ip_address),
                'mask': str(self.mask),
                'date_of_creation': self.date_of_creation.strftime("%d/%m/%y %H:%M"),
                'text': self.text,
                'marks': list(self.marks),
                'ID': self.ID}

    @staticmethod
    def from_json(json_dict):
        n = Note()
        n.ip_address = IPv4Address(json_dict['ip_address'])
        n.mask = IPv4Address(json_dict['mask'])
        n.date_of_creation = datetime.strptime(json_dict['date_of_creation'], "%d/%m/%y %H:%M")
        n.text = json_dict['text']
        n.marks = set(json_dict['marks'])
        n.ID = int(json_dict['ID'])
        return n

    def __copy__(self):
        n = Note()
        n.ip_address = self.ip_address
        n.mask = self.mask
        n.marks = self.marks.copy()
        n.text = self.text
        n.date_of_creation = self.date_of_creation
        n.ID = -1

    def __eq__(self, other):
        if isinstance(other, Note):
            return self.ID == other.ID
        else:
            _logger.error("other is not ipnotebook.program.Note class")
            raise Exception("other is not ipnotebook.program.Note class")

    def __repr__(self):
        return f"<{self.__class__} ID={self.ID} ip_address={self.ip_address} mask={self.mask} date_of_creation={self.date_of_creation} marks={self.marks} text={self.text}>"


class NoteBook(QObject):
    """notebook"""
    changeEvent = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._notes = []  # of ipnotebook.program.
        self._auto_increment_id = 0

    def to_json(self):
        return {'_auto_increment_id': self._auto_increment_id, '_notes': [x.to_json() for x in self._notes]}

    @staticmethod
    def from_json(json_dict):
        n = NoteBook()
        n._auto_increment_id = int(json_dict['_auto_increment_id'])
        for an in json_dict['_notes']:
            n._notes.append(Note.from_json(an))
        return n

    def get_all_notes(self, exclusion_marks: set = None):
        if exclusion_marks is None:
            exclusion_marks = set()
        res = []
        for n in self._notes:
            if len(exclusion_marks) > 0 and len(exclusion_marks.intersection(n.marks)) > 0:
                pass
            else:
                res.append(n)
        return res

    def get_all_marks(self):
        marks_list = set()
        for n in self._notes:
            marks_list.update(set(n.marks))
        return marks_list

    def get_note(self, id: int) -> Note:
        for n in self._notes:
            if n.ID == id:
                return n
        _logger.error('note with ID = ' + str(id) + 'does not exist')
        raise 'note with ID = ' + str(id) + 'does not exist'

    def add_note(self, ip_str, mask_str, date_of_creation, marks_str, text_str):
        marks = self._pars_marks(marks_str)
        if data_validation.is_valid_ipaddress(ip_str) and \
                data_validation.is_valid_mask(mask_str) and \
                data_validation.is_valid_marks(marks) and \
                data_validation.is_valid_text(text_str):
            raise DataDontValidException()
        note = Note(IPv4Address(ip_str), IPv4Address(mask_str), date_of_creation, text_str, set(marks))
        if note.ID != -1:
            _logger.error(f"add {note} is not available. ID != -1")
            raise DataDontValidException('add is not available')
        note.ID = self._get_new_id()
        self._notes.append(note)
        self.changeEvent.emit()

    # TDD
    def update_note(self, note_id, marks_str, text_str):
        """Refreshes the data in the note.

        :param note_id: int - ipnotebook.program.Note.ID
        :param marks_str: string of marks. for example: "dog cat lamp door" - it is 4 marks
        :param text_str: string of text. for example: "This is very important data."
        :return: None
        :except ipnotebook.program.DataDontValidException: incorrect data entered
        """
        n = self.get_note(note_id)
        marks = self._pars_marks(marks_str)
        if not data_validation.is_valid_marks(marks):
            raise DataDontValidException()
        n.marks = set(marks)
        if not data_validation.is_valid_text(text_str):
            raise DataDontValidException()
        n.text = text_str

    def remove_note(self, note_id: int):
        for n in self._notes:
            if n.ID == note_id:
                self._notes.remove(n)
                self.changeEvent.emit()
                break

    def full_text_search(self, q):
        res = []
        for n in self._notes:
            if (str(n.ip_address)+str(n.mask)+n.date_of_creation.strftime(configs['main']['strftime_format'])+n.text+str(n.marks)).find(q) >= 0:
                res.append(n)
        return res

    def _get_new_id(self):
        self._auto_increment_id += 1
        return self._auto_increment_id

    @staticmethod
    def _pars_marks(marks_str) -> list:
        marks = marks_str.strip().split(' ')
        try:
            marks.remove('')
        except ValueError:
            pass
        return marks
