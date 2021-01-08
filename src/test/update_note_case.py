import json
import unittest
import os
import logging
from ipnotebook.program import NoteBook
from ipnotebook.program import DataDontValidException


logging.root.setLevel(logging.INFO)


class NumberOfMarksCase(unittest.TestCase):
    """ Тест количества меток """
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_marks_0(self):
        note_id = 1
        try:
            self._notebook.update_note(note_id, '', '')
            self.assertEqual(self._notebook.get_note(note_id).marks, set())
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_marks_1(self):
        marks_set = {'a'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_marks_10(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertEqual(self._notebook.get_note(note_id).marks, marks_set)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_marks_11(self):
        marks_set = {'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertTrue(False, "тест не пройден. не было исключения о некоррестных введенных данных")
        except DataDontValidException:
            self.assertTrue(True, "тест пройден. вернули исключение, как и положено")


class LengthOfMarksCase(unittest.TestCase):
    """ Тест длины метки """
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_length_1(self):
        marks_set = {'a'}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertEqual(len(self._notebook.get_note(note_id).marks.pop()), 1)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_length_16(self):
        marks_set = {'a'*16}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertEqual(len(self._notebook.get_note(note_id).marks.pop()), 16)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_length_17(self):
        marks_set = {'a'*17}
        marks_str = ' '.join(marks_set)
        note_id = 1
        try:
            self._notebook.update_note(note_id, marks_str, '')
            self.assertTrue(False, "тест не пройден. не было исключения о некоррестных введенных данных")
        except DataDontValidException:
            self.assertTrue(True, "тест пройден. вернули исключение, как и положено")


class LengthTextCase(unittest.TestCase):
    """ Тест длины тестовой заметки """
    def setUp(self) -> None:
        with open(os.path.join('resources', 'test.ntip'), 'r') as f:
            json_dict = json.load(fp=f)
        self._notebook = NoteBook.from_json(json_dict)

    def test_length_0(self):
        text = ""
        note_id = 1
        try:
            self._notebook.update_note(note_id, '', text)
            self.assertEqual(len(self._notebook.get_note(note_id).text), 0)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_length_10000(self):
        text = "a"*10000
        note_id = 1
        try:
            self._notebook.update_note(note_id, '', text)
            self.assertEqual(len(self._notebook.get_note(note_id).text), 10000)
            self.assertTrue(True)
        except DataDontValidException:
            self.assertTrue(False)

    def test_length_10001(self):
        text = "a"*10001
        note_id = 1
        try:
            self._notebook.update_note(note_id, '', text)
            self.assertTrue(False, "тест не пройден. не вызвано исключение на некорректных данных")
        except DataDontValidException:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
