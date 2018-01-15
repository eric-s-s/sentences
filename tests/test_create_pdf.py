import datetime
import os
from shutil import rmtree
import unittest

from reportlab.pdfgen.canvas import Canvas

from sentences.create_pdf import (get_file_prefix, is_numbered_member_of_prefix_group,
                                  insert_footer, save_paragraphs_to_pdf, create_pdf)


SAVE_FOLDER = 'delete_me_dir'


def make_save_folder():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)


def rm_save_folder():
    if os.path.exists(SAVE_FOLDER):
        rmtree(SAVE_FOLDER)


class TestCreatePDF(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        rm_save_folder()

    def setUp(self):
        make_save_folder()
        self.error = 'This are a wrong sentence. So are this.'
        self.answer = 'This <bold>is</bold> a wrong sentence. So <bold>is</bold> this.  -- error count: 2'

    def tearDown(self):
        rm_save_folder()

    def test_is_numbered_member_of_prefix_group_true(self):
        self.assertTrue(is_numbered_member_of_prefix_group('01_thing.pdf', prefix=''))
        self.assertTrue(is_numbered_member_of_prefix_group('10_thing.pdf', prefix=''))
        self.assertTrue(is_numbered_member_of_prefix_group('99_thing.pdf', prefix=''))
        self.assertTrue(is_numbered_member_of_prefix_group('00_thing.pdf', prefix=''))
        self.assertTrue(is_numbered_member_of_prefix_group('01_thing.txt', prefix=''))

    def test_is_numbered_member_of_prefix_group_false(self):
        self.assertFalse(is_numbered_member_of_prefix_group('1_thing.pdf', prefix=''))
        self.assertFalse(is_numbered_member_of_prefix_group('100_thing.pdf', prefix=''))
        self.assertFalse(is_numbered_member_of_prefix_group('01 thing.pdf', prefix=''))
        self.assertFalse(is_numbered_member_of_prefix_group('thing.pdf', prefix=''))

    def test_get_file_prefix_no_files(self):
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '01_')

    def test_get_file_prefix_no_named_prefix(self):
        file_names = ['not_pdf.txt', '01_text.txt', '1_too_few_digits.pdf', '010_too_many_digits.pdf',
                      '01 no_underscore.pdf', 'no_digits.pdf']
        for filename in file_names:
            with open(os.path.join(SAVE_FOLDER, filename), 'w') as f:
                f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '02_')

        with open(os.path.join(SAVE_FOLDER, '02_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '03_')

        with open(os.path.join(SAVE_FOLDER, '09_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '10_')

        with open(os.path.join(SAVE_FOLDER, '29_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '30_')

    def test_get_file_prefix_with_named_prefix_ignores_others(self):
        file_names = ['prefix_01_stuff.txt', '05_stuff.txt', 'oopsy11.txt']
        for filename in file_names:
            with open(os.path.join(SAVE_FOLDER, filename), 'w') as f:
                f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER, 'prefix_'), 'prefix_02_')

    def test_insert_footer(self):
        class Doc(object):
            def __init__(self):
                self.title = 'fake title'
                self.page = 3

        now_to_hour = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')
        canvas = Canvas(os.path.join(SAVE_FOLDER, 'dummy.pdf'))
        insert_footer(canvas, Doc())
        content = canvas.getCurrentPageContent()
        self.assertIn('fake title : page 3, {}'.format(now_to_hour), content)

    def test_save_paragraph_to_pdf_saves_file(self):
        file_name = os.path.join(SAVE_FOLDER, 'test.pdf')
        self.assertFalse(os.path.exists(file_name))
        save_paragraphs_to_pdf(file_name, self.error, 10)

        self.assertTrue(os.path.exists(file_name))

    def test_create_pdfs_saves_files(self):
        error_1 = os.path.join(SAVE_FOLDER, '01_error.pdf')
        error_2 = os.path.join(SAVE_FOLDER, '02_error.pdf')
        answer_1 = os.path.join(SAVE_FOLDER, '01_answer.pdf')
        answer_2 = os.path.join(SAVE_FOLDER, '02_answer.pdf')
        for file_name in (error_1, error_2, answer_1, answer_2):
            self.assertFalse(os.path.exists(file_name))

        create_pdf(SAVE_FOLDER, self.answer, self.error)
        self.assertTrue(os.path.exists(error_1))
        self.assertTrue(os.path.exists(answer_1))
        self.assertFalse(os.path.exists(error_2))
        self.assertFalse(os.path.exists(answer_2))

        create_pdf(SAVE_FOLDER, self.answer, self.error)
        for file_name in (error_1, error_2, answer_1, answer_2):
            self.assertTrue(os.path.exists(file_name))

    def test_create_pdfs_saves_files_with_named_prefix(self):
        error_1 = os.path.join(SAVE_FOLDER, 'bob01_error.pdf')
        error_2 = os.path.join(SAVE_FOLDER, 'bob02_error.pdf')
        answer_1 = os.path.join(SAVE_FOLDER, 'bob01_answer.pdf')
        answer_2 = os.path.join(SAVE_FOLDER, 'bob02_answer.pdf')

        other_answer = os.path.join(SAVE_FOLDER, 'joe_01_answer.pdf')
        other_error = os.path.join(SAVE_FOLDER, 'joe_01_error.pdf')

        for file_name in (error_1, error_2, answer_1, answer_2, other_answer, other_error):
            self.assertFalse(os.path.exists(file_name))

        create_pdf(SAVE_FOLDER, self.answer, self.error, named_prefix='bob')
        for file_name in (error_1, answer_1):
            self.assertTrue(os.path.exists(file_name))
        for file_name in (error_2, answer_2, other_answer, other_error):
            self.assertFalse(os.path.exists(file_name))

        create_pdf(SAVE_FOLDER, self.answer, self.error, named_prefix='joe_')
        for file_name in (error_1, answer_1, other_answer, other_error):
            self.assertTrue(os.path.exists(file_name))
        for file_name in (error_2, answer_2):
            self.assertFalse(os.path.exists(file_name))

        create_pdf(SAVE_FOLDER, self.answer, self.error, named_prefix='bob')
        for file_name in (error_1, error_2, answer_1, answer_2):
            self.assertTrue(os.path.exists(file_name))

