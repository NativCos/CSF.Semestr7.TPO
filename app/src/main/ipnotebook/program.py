"""
Business logic
"""
from datetime import datetime
from ipaddress import IPv4Address
import logging

_logger = logging.getLogger("ipnotebook.program")
_logger.setLevel(logging.DEBUG)


FILENAME_EXTENSION = 'ntip'


class Note:
    """one note about ip address"""
    ip_address = IPv4Address('0.0.0.0')
    mask = IPv4Address('0.0.0.0')
    date_of_creation = datetime.now()
    text = ""
    marks = []

    def toJSON(self):
        return {'ip_address':str(self.ip_address),
                'mask':str(self.mask),
                'date_of_creation':self.date_of_creation.strftime("%d/%m/%y %H:%M"),
                'text':self.text,
                'marks':self.marks}

    @staticmethod
    def fromJSON(json_dict):
        n = Note()
        n.ip_address = IPv4Address(json_dict['ip_address'])
        n.mask = IPv4Address(json_dict['mask'])
        n.date_of_creation = datetime.strptime(json_dict['date_of_creation'], "%d/%m/%y %H:%M")
        n.text = json_dict['text']
        n.marks = json_dict['marks']
        return n


class NoteBook:
    """notebook"""
    notes = []  # of ipnotebook.program.Note

    def toJSON(self):
        return [x.toJSON() for x in self.notes]

    @staticmethod
    def fromJSON(json_dict):
        n = NoteBook()
        for an in json_dict:
            n.notes.append(Note.fromJSON(an))
        return n


