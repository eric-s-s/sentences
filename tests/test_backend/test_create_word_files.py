import unittest

from shutil import rmtree
import os

from sentences import DATA_PATH, VERBS_CSV, UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV
from sentences.backend.create_word_files import create_default_word_files, move_to_old


DIR_TO_DELETE = "dir_to_delete"


def rm_test_dir():
    if os.path.exists(DIR_TO_DELETE):
        rmtree(DIR_TO_DELETE)


def copy_all_csv():
    for filename in (VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV):
        with open(os.path.join(DATA_PATH, filename), 'r') as read_file:
            with open(os.path.join(DIR_TO_DELETE, filename), 'w') as write_file:
                write_file.write(read_file.read())


class TestCreateWordFiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rm_test_dir()

    @classmethod
    def tearDownClass(cls):
        rm_test_dir()

    def setUp(self):
        os.mkdir(DIR_TO_DELETE)
        copy_all_csv()

    def tearDown(self):
        rm_test_dir()

    def test_move_to_old_no_old_files(self):

        original_path = os.path.join(DIR_TO_DELETE, VERBS_CSV)
        new_path = os.path.join(DIR_TO_DELETE, VERBS_CSV.replace('.csv', '_old_01.csv'))
        self.assertTrue(os.path.exists(original_path))
        self.assertFalse(os.path.exists(new_path))

        move_to_old(DIR_TO_DELETE, VERBS_CSV)

        self.assertTrue(os.path.exists(original_path))  # TODO
        self.assertTrue(os.path.exists(new_path))

        with open(os.path.join(DATA_PATH, VERBS_CSV), 'r') as original_file:
            with open(new_path, 'r') as new_file:
                self.assertEqual(original_file.read(), new_file.read())


