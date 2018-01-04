import datetime
import os
from shutil import rmtree
import unittest

from reportlab.pdfgen.canvas import Canvas

from sentences.create_pdf import get_file_prefix, is_numbered_pdf, insert_footer


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

    def test_is_numbered_pdf_true(self):
        self.assertTrue(is_numbered_pdf('01_thing.pdf'))
        self.assertTrue(is_numbered_pdf('10_thing.pdf'))
        self.assertTrue(is_numbered_pdf('99_thing.pdf'))
        self.assertTrue(is_numbered_pdf('00_thing.pdf'))

    def test_is_numbered_pdf_false(self):
        self.assertFalse(is_numbered_pdf('1_thing.pdf'))
        self.assertFalse(is_numbered_pdf('100_thing.pdf'))
        self.assertFalse(is_numbered_pdf('01 thing.pdf'))
        self.assertFalse(is_numbered_pdf('thing.pdf'))
        self.assertFalse(is_numbered_pdf('01_thing.txt'))

    def test_get_file_prefix_no_files(self):
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '01_')

    def test_get_file_prefix_no_numbered_pdf_files(self):
        filenames = ['not_pdf.txt', '01_text.txt', '1_too_few_digits.pdf', '010_too_many_digits.pdf',
                     '01 no_underscore.pdf', 'no_digits.pdf']
        for filename in filenames:
            with open(os.path.join(SAVE_FOLDER, filename), 'w') as f:
                f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '01_')

    def test_get_file_prefix_numbered_pdf(self):
        with open(os.path.join(SAVE_FOLDER, '02_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '03_')

        with open(os.path.join(SAVE_FOLDER, '09_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '10_')

        with open(os.path.join(SAVE_FOLDER, '29_thing.pdf'), 'w') as f:
            f.write('ipso lorum')
        self.assertEqual(get_file_prefix(SAVE_FOLDER), '30_')

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
