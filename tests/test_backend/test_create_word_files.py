import unittest

import shutil
import os

from sentences import DATA_PATH, VERBS_CSV, UNCOUNTABLE_NOUNS_CSV, COUNTABLE_NOUNS_CSV
from sentences.backend.create_word_files import create_default_word_files, copy_to_numbered_old_file

from tests import TESTS_FILES


DIR_TO_DELETE = os.path.join(TESTS_FILES, 'dir_to_delete')


def rm_test_dir():
    if os.path.exists(DIR_TO_DELETE):
        shutil.rmtree(DIR_TO_DELETE)


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

    def test_copy_to_numbered_old_file_no_old_files(self):
        original_path = os.path.join(DIR_TO_DELETE, VERBS_CSV)
        new_path = os.path.join(DIR_TO_DELETE, VERBS_CSV.replace('.csv', '_old_01.csv'))
        self.assertTrue(os.path.exists(original_path))
        self.assertFalse(os.path.exists(new_path))

        copy_to_numbered_old_file(DIR_TO_DELETE, VERBS_CSV)

        self.assertTrue(os.path.exists(original_path))
        self.assertTrue(os.path.exists(new_path))

        with open(os.path.join(DATA_PATH, VERBS_CSV), 'r') as original_file:
            with open(new_path, 'r') as new_file:
                self.assertEqual(original_file.read(), new_file.read())

    def test_copy_to_numbered_old_file_differently_named_old_files(self):
        copy_to_numbered_old_file(DIR_TO_DELETE, VERBS_CSV)
        copy_to_numbered_old_file(DIR_TO_DELETE, COUNTABLE_NOUNS_CSV)

        exists = os.path.join(DIR_TO_DELETE, COUNTABLE_NOUNS_CSV.replace('.csv', '_old_01.csv'))
        does_not_exist = os.path.join(DIR_TO_DELETE, COUNTABLE_NOUNS_CSV.replace('.csv', '_old_02.csv'))

        self.assertTrue(os.path.exists(exists))
        self.assertFalse(os.path.exists(does_not_exist))

        with open(os.path.join(DATA_PATH, COUNTABLE_NOUNS_CSV), 'r') as original_file:
            with open(exists, 'r') as new_file:
                self.assertEqual(original_file.read(), new_file.read())

    def test_copy_to_numbered_old_multiple_files_and_formatting_above_ten(self):
        expected = []
        for number in range(1, 10):
            replace_str = '_old_0{}.csv'.format(number)
            new_file = os.path.join(DIR_TO_DELETE, VERBS_CSV.replace('.csv', replace_str))
            expected.append(new_file)
        for number in range(10, 12):
            replace_str = '_old_{}.csv'.format(number)
            new_file = os.path.join(DIR_TO_DELETE, VERBS_CSV.replace('.csv', replace_str))
            expected.append(new_file)

        for index in range(1, 13):
            copy_to_numbered_old_file(DIR_TO_DELETE, VERBS_CSV)
            exists = expected[:index]
            does_not_exists = expected[index:]
            self.assertTrue(all(os.path.exists(file) for file in exists))
            self.assertFalse(any(os.path.exists(file) for file in does_not_exists))

    def test_copy_to_numbered_old_file_unreadable_file(self):
        bad_file = os.path.join(DIR_TO_DELETE, 'oops.csv')
        shutil.copy(os.path.join(DATA_PATH, 'go_time.ico'), bad_file)
        copy_to_numbered_old_file(DIR_TO_DELETE, 'oops.csv')
        with open(bad_file.replace('.csv', '_old_01.csv'), 'r') as f:
            self.assertEqual(f.read(), '')

    def test_create_default_word_files_empty_dir(self):
        expected = (VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV)
        for filename in expected:
            os.remove(os.path.join(DIR_TO_DELETE, filename))

        create_default_word_files(DIR_TO_DELETE)

        for filename in expected:
            with open(os.path.join(DATA_PATH, filename), 'r') as original_file:
                with open(os.path.join(DIR_TO_DELETE, filename), 'r') as new_file:
                    self.assertEqual(original_file.read(), new_file.read())

    def test_create_default_word_files_some_files_missing(self):
        expected = (VERBS_CSV, COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV)

        with open(os.path.join(DIR_TO_DELETE, COUNTABLE_NOUNS_CSV), 'w') as f:
            f.write('new file')
        os.remove(os.path.join(DIR_TO_DELETE, VERBS_CSV))

        create_default_word_files(DIR_TO_DELETE)

        for filename in expected:
            with open(os.path.join(DATA_PATH, filename), 'r') as original_file:
                with open(os.path.join(DIR_TO_DELETE, filename), 'r') as new_file:
                    self.assertEqual(original_file.read(), new_file.read())

        old_verb = VERBS_CSV.replace('.csv', '_old_01.csv')
        old_countable = COUNTABLE_NOUNS_CSV.replace('.csv', '_old_01.csv')
        old_uncountable = UNCOUNTABLE_NOUNS_CSV.replace('.csv', '_old_01.csv')
        with open(os.path.join(DIR_TO_DELETE, old_countable), 'r') as f:
            self.assertEqual(f.read(), 'new file')
        self.assertFalse(os.path.exists(os.path.join(DIR_TO_DELETE, old_verb)))
        self.assertTrue(os.path.exists(os.path.join(DIR_TO_DELETE, old_uncountable)))

    def test_create_default_word_files_multiple_calls(self):
        with open(os.path.join(DIR_TO_DELETE, VERBS_CSV), 'w') as f:
            f.write('trace')

        create_default_word_files(DIR_TO_DELETE)
        create_default_word_files(DIR_TO_DELETE)
        create_default_word_files(DIR_TO_DELETE)

        with open(os.path.join(DATA_PATH, VERBS_CSV), 'r') as f:
            original_text = f.read()

        for count in range(1, 4):
            filename = VERBS_CSV.replace('.csv', '_old_0{}.csv'.format(count))
            with open(os.path.join(DIR_TO_DELETE, filename), 'r') as f:
                old_text = f.read()
            if count == 1:
                self.assertEqual(old_text, 'trace')
            else:
                self.assertEqual(old_text, original_text)
