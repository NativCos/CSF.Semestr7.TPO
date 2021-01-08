import json
import unittest
import os
import logging
from ipnotebook.program import NoteBook
from ipnotebook.program import DataDontValidException


logging.root.setLevel(logging.ERROR)


class UpdateNoteCase(unittest.TestCase):
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_update_0(self):
        note_id = 1
        self._notebook.update_note(note_id, '', '')
        self.assertEqual(self._notebook.get_note(note_id).marks, set())

    def test_update_1(self):
        marks_set = {'q'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self._notebook.update_note(note_id, marks_str, '')
        self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)

    def test_update_10(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        self._notebook.update_note(note_id, marks_str, '')
        self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)

    def test_update_11(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertTrue(False)  # тест не пройден. не было исключения о некоррестных введенных данных
        except DataDontValidException:
            self.assertTrue(True)  # тест пройден. вернули исключение, как и положено


if __name__ == '__main__':
    unittest.main()
