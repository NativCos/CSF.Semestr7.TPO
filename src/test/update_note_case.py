import json
import unittest
import os
import logging
from ipnotebook.program import NoteBook
from ipnotebook.program import DataDontValidException


logging.root.setLevel(logging.INFO)


""" *ПИТОНИСТ* - нецензурная интонация))))
    ИЗНАСИЛОВАЛ ООП
    ЭТО ДОЛЖЕН БЫТЬ ИНТЕГРАЦИОННЫЙ ТЕСТ!!!! А НЕ UNIT! ТЫ ЧО ТВОРИШЬ! ПОСМОТРИ КАК ФУНКЦИИ ИСПОЛЬЗУЮТСЯ !
    используй assertRaise!
"""


class MarksCase(unittest.TestCase):
    """ Тест меток """
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_number_0(self):
        note_id = 1
        self._notebook.update_note(note_id, '', '')
        self.assertEqual(self._notebook.get_note(note_id).marks, set())

    def test_number_10_len_1(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self._notebook.update_note(note_id, marks_str, '')
        self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)

    def test_number_10_len_16(self):
        marks_set = {'q'*16, 'w'*16, 'e'*16, 'r'*16, 't'*16, 'y'*16, 'u'*16, 'i'*16, 'o'*16, 'p'*16}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self._notebook.update_note(note_id, marks_str, '')
        self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)

    def test_number_10_len_17(self):
        marks_set = {'q'*17, 'w'*17, 'e'*17, 'r'*17, 't'*17, 'y'*17, 'u'*17, 'i'*17, 'o'*17, 'p'*17}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self.assertRaises(DataDontValidException, self._notebook.update_note, note_id, marks_str, '')

    def test_number_11_len_1(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'm'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self.assertRaises(DataDontValidException, self._notebook.update_note, note_id, marks_str, '')


class LengthTextCase(unittest.TestCase):
    """ Тест длины тестовой заметки """
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_length_0(self):
        text = ""
        note_id = 1
        self._notebook.update_note(note_id, '', text)
        self.assertEqual(len(self._notebook.get_note(note_id).text), 0)

    def test_length_10000(self):
        text = "a"*10000
        note_id = 1
        self._notebook.update_note(note_id, '', text)
        self.assertEqual(len(self._notebook.get_note(note_id).text), 10000)

    def test_length_10001(self):
        text = "a"*10001
        note_id = 1
        self.assertRaises(DataDontValidException, self._notebook.update_note, note_id, '', text)


if __name__ == '__main__':
    unittest.main()
