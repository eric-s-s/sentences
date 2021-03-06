import unittest
from random import seed
import os

from sentences.paragraphsgenerator import ParagraphsGenerator

from sentences import COUNTABLE_NOUNS_CSV, UNCOUNTABLE_NOUNS_CSV, PROPER_NOUNS_CSV, VERBS_CSV
from sentences.backend.loader import verbs, uncountable_nouns, countable_nouns, proper_nouns
from sentences.words.pronoun import Pronoun, CapitalPronoun
from sentences.words.noun import Noun
from sentences.words.verb import Verb
from sentences.words.punctuation import Punctuation

from tests import TESTS_FILES

period = Punctuation.PERIOD
exclamation = Punctuation.EXCLAMATION

i, me, you, he, him, she, her, it, we, us, they, them = Pronoun.__members__.values()


delete_me = os.path.join(TESTS_FILES, 'delete_me_{}')

DELETE_ME_VERBS = delete_me.format(VERBS_CSV)
DELETE_ME_COUNTABLE = delete_me.format(COUNTABLE_NOUNS_CSV)
DELETE_ME_UNCOUNTABLE = delete_me.format(UNCOUNTABLE_NOUNS_CSV)
DELETE_ME_PROPER = delete_me.format(PROPER_NOUNS_CSV)


def line_print(long_text, lin_len):
    new = '("' + long_text[:lin_len] + '" +\n'
    long_text = long_text[lin_len:]
    while long_text:
        new += ' "' + long_text[:lin_len] + '" +\n'
        long_text = long_text[lin_len:]
    new = new[:-3] + '),'
    print(new)


def short_line_print(short_text):
    print('"{}",'.format(short_text))


def create_test_csvs(countable_list, uncountable_list, verb_list, proper_list):
    countable_text = '\n'.join(countable_list)
    uncountable_text = '\n'.join(uncountable_list)
    proper_text = '\n'.join([line + ',s' for line in proper_list])
    verb_text = '\n'.join(verb_list)
    for filename, text in zip((DELETE_ME_VERBS, DELETE_ME_COUNTABLE, DELETE_ME_UNCOUNTABLE, DELETE_ME_PROPER),
                              (verb_text, countable_text, uncountable_text, proper_text)):
        with open(filename, 'w') as f:
            f.write(text)


def create_single_value_test_csvs(dummy_word):
    create_test_csvs([dummy_word], ['uncountable {}'.format(dummy_word)], [dummy_word], [dummy_word.capitalize()])


def delete_test_csvs():
    for path in (DELETE_ME_VERBS, DELETE_ME_COUNTABLE, DELETE_ME_UNCOUNTABLE, DELETE_ME_PROPER):
        if os.path.exists(path):
            os.remove(path)


class TestParagraphGenerator(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        delete_test_csvs()

    def setUp(self):
        create_test_csvs(['dog', 'cat'], ['water', 'milk'], ['like', 'use'], ['Bob', 'Joe'])

        self.config_state = {
            'home_directory': '',
            'save_directory': '',
            'countable_nouns': DELETE_ME_COUNTABLE,
            'uncountable_nouns': DELETE_ME_UNCOUNTABLE,
            'proper_nouns': DELETE_ME_PROPER,
            'verbs': DELETE_ME_VERBS,

            'error_probability': 0.2,
            'noun_errors': True,
            'pronoun_errors': False,
            'verb_errors': True,
            'punctuation_errors': True,
            'is_do_errors': False,
            'preposition_transpose_errors': False,

            'tense': 'simple_present',
            'probability_plural_noun': 0.3,
            'probability_negative_verb': 0.3,
            'probability_pronoun': 0.2,

            'paragraph_type': 'chain',
            'subject_pool': 5,
            'num_paragraphs': 4,
            'paragraph_size': 15,
        }

    def test_create_test_csvs(self):
        values = (['a', 'b'], ['b', 'c'], ['d', 'e'], ['f', 'g'])
        expected = ['a\nb', 'b\nc', 'd\ne', 'f,s\ng,s']
        create_test_csvs(*values)
        for index, filename in enumerate((DELETE_ME_COUNTABLE, DELETE_ME_UNCOUNTABLE,
                                          DELETE_ME_VERBS, DELETE_ME_PROPER)):
            with open(filename, 'r') as f:
                self.assertEqual(expected[index], f.read())

    def test_create_single_value_csvs(self):
        create_single_value_test_csvs('ab')
        expected = ['ab', 'uncountable ab', 'ab', 'Ab,s']
        for index, filename in enumerate((DELETE_ME_COUNTABLE, DELETE_ME_UNCOUNTABLE,
                                          DELETE_ME_VERBS, DELETE_ME_PROPER)):
            with open(filename, 'r') as f:
                self.assertEqual(expected[index], f.read())

    def test_init_loads_in_csv_paths(self):
        pg = ParagraphsGenerator(self.config_state)
        self.assertEqual(pg._verbs_list, verbs(DELETE_ME_VERBS))
        all_nouns = (
            countable_nouns(DELETE_ME_COUNTABLE) +
            uncountable_nouns(DELETE_ME_UNCOUNTABLE) +
            proper_nouns(DELETE_ME_PROPER)
        )
        self.assertEqual(pg._nouns_list, all_nouns)

    def assert_single_value_word_list(self, paragraph_generator, dummy_word):
        self.assertEqual(paragraph_generator._verbs_list[0]['verb'], Verb(dummy_word))
        self.assertEqual(paragraph_generator._nouns_list[0], Noun(dummy_word))
        self.assertEqual(paragraph_generator._nouns_list[1], Noun.uncountable_noun('uncountable {}'.format(dummy_word)))
        self.assertEqual(paragraph_generator._nouns_list[2], Noun.proper_noun(dummy_word.capitalize()))

    def test_load_csv_reloads(self):
        create_single_value_test_csvs('cat')
        pg = ParagraphsGenerator(self.config_state)
        self.assert_single_value_word_list(pg, 'cat')

        create_single_value_test_csvs('dog')
        pg.load_lists_from_file()
        self.assert_single_value_word_list(pg, 'dog')

    def test_update_options_empty_dict_does_not_change_dict_does_not_reload_files(self):
        create_single_value_test_csvs('dog')
        pg = ParagraphsGenerator(self.config_state)
        create_single_value_test_csvs('cat')
        pg.update_options({})
        self.assertEqual(pg._options, self.config_state)
        self.assert_single_value_word_list(pg, 'dog')

    def test_update_options_updates_dict(self):
        pg = ParagraphsGenerator(self.config_state)
        self.assertEqual(pg._options, self.config_state)

        pg.update_options({'paragraph_size': 10})
        self.config_state['paragraph_size'] = 10
        self.assertEqual(pg._options, self.config_state)

    def test_update_options_reloads_lists_if_any_are_None(self):
        create_single_value_test_csvs('cat')
        pg = ParagraphsGenerator(self.config_state)
        pg._verbs_list = []

        create_single_value_test_csvs('dog')
        pg.update_options({'dummy': 10})
        self.assert_single_value_word_list(pg, 'dog')

    def test_update_options_reloads_lists_if_any_filenames_change(self):
        create_single_value_test_csvs('cat')
        pg = ParagraphsGenerator(self.config_state)

        create_single_value_test_csvs('dog')
        pg._options['verbs'] = 'oops'
        pg.update_options({'verbs': DELETE_ME_VERBS})
        self.assert_single_value_word_list(pg, 'dog')

        create_single_value_test_csvs('cat')
        pg._options['countable_nouns'] = 'oops'
        pg.update_options({'countable_nouns': DELETE_ME_COUNTABLE})
        self.assert_single_value_word_list(pg, 'cat')

        create_single_value_test_csvs('dog')
        pg._options['uncountable_nouns'] = 'oops'
        pg.update_options({'uncountable_nouns': DELETE_ME_UNCOUNTABLE})
        self.assert_single_value_word_list(pg, 'dog')

    def test_update_options_does_not_reload_list_if_file_names_are_not_changed(self):
        create_single_value_test_csvs('dog')
        pg = ParagraphsGenerator(self.config_state)
        to_change = {key: None for key in self.config_state if key not in
                     ('verbs', 'countable_nouns', 'uncountable_nouns', 'proper_nouns')}
        create_single_value_test_csvs('cat')
        pg.update_options(to_change)
        self.assert_single_value_word_list(pg, 'dog')

    def test_create_paragraph_probability_pronoun(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])
        self.config_state['probability_pronoun'] = 0.0

        pg = ParagraphsGenerator(self.config_state)
        for _ in range(10):
            paragraph = pg.create_paragraph()
            for sentence in paragraph:
                self.assertIsInstance(sentence[0], Noun)
                self.assertIsInstance(sentence[2], Noun)

        pg.update_options({'probability_pronoun': 1.0})
        for _ in range(10):
            paragraph = pg.create_paragraph()
            for sentence in paragraph:
                self.assertIsInstance(sentence[0], CapitalPronoun)
                self.assertIsInstance(sentence[2], Pronoun)

    def test_create_paragraph_paragraph_size(self):
        self.config_state['paragraph_size'] = 5
        pg = ParagraphsGenerator(self.config_state)
        for _ in range(3):
            self.assertEqual(len(pg.create_paragraph()), 5)

        pg.update_options({'paragraph_size': 2})
        for _ in range(3):
            self.assertEqual(len(pg.create_paragraph()), 2)

    def test_create_paragraph_word_lists(self):
        seed(1234)
        create_test_csvs(['dog'], ['water'], ['like'], ['Frank'])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['paragraph_size'] = 2

        pg = ParagraphsGenerator(self.config_state)

        raw_answer = pg.create_paragraph()
        answer = [[word.value for word in sentence] for sentence in raw_answer]
        self.assertEqual(answer, [['Water', "doesn't like", 'Frank', '.'], ['Frank', 'likes', 'the water', '.']])

        raw_answer = pg.create_paragraph()
        answer = [[word.value for word in sentence] for sentence in raw_answer]
        self.assertEqual(answer, [['Frank', "doesn't like", 'a dog', '.'], ['The dog', 'likes', 'Frank', '.']])

        raw_answer = pg.create_paragraph()
        answer = [[word.value for word in sentence] for sentence in raw_answer]
        self.assertEqual(answer, [['Water', 'likes', 'Frank', '!'], ['Frank', 'likes', 'a dog', '.']])

    def test_create_paragraph_pool_paragraph(self):
        seed(8908)
        create_test_csvs(['dog', 'cat'], ['water'], ['like'], ['My Great-Aunt Fanny'])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['paragraph_type'] = 'pool'
        self.config_state['subject_pool'] = 1

        pg = ParagraphsGenerator(self.config_state)
        answer = pg.create_paragraph()
        for sentence in answer:
            self.assertIn('cat', sentence[0].value)
            self.assertIsInstance(sentence[2], Noun)
            self.assertNotIn('cat', sentence[2].value)

        pg.update_options({'subject_pool': 2})
        answer = pg.create_paragraph()
        values = ['Water', 'The water', 'My Great-Aunt Fanny']
        for sentence in answer:
            self.assertIn(sentence[0].value, values)
            self.assertIsInstance(sentence[2], Noun)

    def test_create_paragraph_chain_paragraph(self):
        seed(4569)
        create_test_csvs(['dog'], ['water'], ['like'], [])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['paragraph_type'] = 'chain'

        pg = ParagraphsGenerator(self.config_state)
        answer = pg.create_paragraph()
        for index, sentence in enumerate(answer):
            if index == 0:
                self.assertEqual(sentence[0].value, 'Water')
                self.assertEqual(sentence[2].value, 'a dog')
            elif index % 2 == 0:
                self.assertEqual(sentence[0].value, 'The water')
                self.assertEqual(sentence[2].value, 'the dog')
            else:
                self.assertEqual(sentence[0].value, 'The dog')
                self.assertEqual(sentence[2].value, 'the water')

    def test_create_paragraph_probability_plural_noun(self):
        create_test_csvs(['dog', 'cat'], ['water'], ['like'], ['Abbey Normal'])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_plural_noun'] = 1.0

        pg = ParagraphsGenerator(self.config_state)
        answer = pg.create_paragraph()
        noun_values = ['Dogs', 'The dogs', 'dogs', 'the dogs',
                       'Cats', 'The cats', 'cats', 'the cats',
                       'Water', 'The water', 'water', 'the water',
                       'Abbey Normal']
        for sentence in answer:
            self.assertIn(sentence[0].value, noun_values)
            self.assertIn(sentence[2].value, noun_values)

        pg.update_options({'probability_plural_noun': 0.0})
        answer = pg.create_paragraph()
        noun_values = ['A dog', 'The dog', 'a dog', 'the dog',
                       'A cat', 'The cat', 'a cat', 'the cat',
                       'Water', 'The water', 'water', 'the water',
                       'Abbey Normal']
        for sentence in answer:
            self.assertIn(sentence[0].value, noun_values)
            self.assertIn(sentence[2].value, noun_values)

    def test_create_paragraph_probability_negative_verb(self):
        create_test_csvs(['dog', 'cat'], ['water'], ['like'], ['Mom'])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_plural_noun'] = 0.0
        self.config_state['probability_negative_verb'] = 1.0

        pg = ParagraphsGenerator(self.config_state)
        answer = pg.create_paragraph()
        verb_value = "doesn't like"
        for sentence in answer:
            self.assertEqual(verb_value, sentence[1].value)

        pg.update_options({'probability_negative_verb': 0.0})
        answer = pg.create_paragraph()
        verb_value = "likes"
        for sentence in answer:
            self.assertEqual(verb_value, sentence[1].value)

    def test_create_paragraph_tense(self):
        create_test_csvs(['dog', 'cat'], ['water'], ['like'], ['Dad'])
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_negative_verb'] = 0.0
        self.config_state['tense'] = 'simple_past'

        pg = ParagraphsGenerator(self.config_state)
        answer = pg.create_paragraph()
        verb_value = "liked"
        for sentence in answer:
            self.assertEqual(verb_value, sentence[1].value)

    def test_create_answer_and_error_texts_error_probability(self):
        self.config_state['error_probability'] = 0.0
        self.config_state['probability_pronoun'] = 0.0

        pg = ParagraphsGenerator(self.config_state)
        for _ in range(5):
            answer, error = pg.create_answer_and_error_texts()
            self.assertEqual(answer, error + ' -- error count: 0')

        pg.update_options({'error_probability': 1.0})
        for _ in range(5):
            answer, error = pg.create_answer_and_error_texts()
            self.assertTrue(answer.endswith(' -- error count: 60'))
            self.assertNotEqual(answer, error + ' -- error count: 60')

    def test_create_answer_and_error_texts_noun_errors(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['probability_plural_noun'] = 0.0
        self.config_state['error_probability'] = 1.0
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['verb_errors'] = False
        self.config_state['punctuation_errors'] = False

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        self.assertEqual(answer.count('<bold>The dog</bold>'), 7)
        self.assertEqual(answer.count('<bold>The water</bold>'), 7)
        self.assertEqual(answer.count('<bold>the dog</bold>'), 7)
        self.assertEqual(answer.count('<bold>the dog</bold>'), 7)
        self.assertTrue(answer.endswith(' -- error count: 30'))

    def test_create_answer_and_error_texts_pronoun_errors(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['error_probability'] = 1.0
        self.config_state['probability_pronoun'] = 1.0
        self.config_state['pronoun_errors'] = True
        self.config_state['verb_errors'] = False
        self.config_state['punctuation_errors'] = False

        seed(34349)

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        expected_answer = (
            "<bold>She</bold> likes <bold>him</bold>. <bold>He</bold> likes <bold>me</bold>! <bold>I</bold> like " +
            "it. It likes <bold>me</bold>. <bold>I</bold> don't like <bold>them</bold>. <bold>They</bold> like it" +
            ". It likes you. You like <bold>us</bold>. <bold>We</bold> like <bold>her</bold>! <bold>She</bold> li" +
            "kes <bold>them</bold>! <bold>They</bold> like <bold>me</bold>. <bold>I</bold> don't like <bold>her</" +
            "bold>! <bold>She</bold> likes <bold>us</bold>. <bold>We</bold> like you! You like <bold>me</bold>. -" +
            "- error count: 22")
        expected_error = (
            "Her likes he. Him likes I! Me like it. It likes I. Me don't like they. Them like it. It likes you. Y" +
            "ou like we. Us like she! Her likes they! Them like I. Me don't like she! Her likes we. Us like you! " +
            "You like I."
        )
        self.assertEqual(answer, expected_answer)
        self.assertEqual(error, expected_error)

    def test_create_answer_and_error_texts_verb_errors(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['probability_negative_verb'] = 0.0
        self.config_state['error_probability'] = 1.0
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_plural_noun'] = 0.0
        self.config_state['noun_errors'] = False
        self.config_state['punctuation_errors'] = False

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        self.assertEqual(answer.count('<bold>likes</bold>'), 15)
        self.assertTrue(answer.endswith(' -- error count: 15'))

    def test_create_answer_and_error_texts_is_do_errors(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['probability_negative_verb'] = 0.0
        self.config_state['error_probability'] = 1.0
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_plural_noun'] = 0.0
        self.config_state['noun_errors'] = False
        self.config_state['punctuation_errors'] = False
        self.config_state['verb_errors'] = False
        self.config_state['is_do_errors'] = True

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        self.assertEqual(answer.count('<bold>likes</bold>'), 15)
        self.assertEqual(error.count('is like'), 15)
        self.assertTrue(answer.endswith(' -- error count: 15'))

    def test_create_answer_and_error_texts_preposition_transpose_errors(self):
        create_test_csvs(['dog'], [''], ['jump, null, on'], [])

        self.config_state['probability_negative_verb'] = 0.0
        self.config_state['error_probability'] = 1.0
        self.config_state['probability_pronoun'] = 0.0
        self.config_state['probability_plural_noun'] = 0.0
        self.config_state['noun_errors'] = False
        self.config_state['punctuation_errors'] = False
        self.config_state['verb_errors'] = False
        self.config_state['preposition_transpose_errors'] = True

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        self.assertEqual(answer.count('<bold>on</bold> <bold>the dog</bold>'), 15)
        self.assertEqual(error.count('The dog on the dog jumps'), 14)
        self.assertTrue(answer.endswith(' -- error count: 15'))

    def test_create_answer_and_error_texts_punctuation_errors(self):
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['error_probability'] = 1.0
        self.config_state['noun_errors'] = False
        self.config_state['verb_errors'] = False

        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        self.assertEqual(error.count(','), 15)
        self.assertTrue(answer.endswith(' -- error count: 15'))

    def test_create_answer_and_error_texts_converts_to_texts(self):
        seed(85690)
        create_test_csvs(['dog'], ['water'], ['like'], [])

        self.config_state['error_probability'] = 1.0
        self.config_state['paragraph_size'] = 2
        pg = ParagraphsGenerator(self.config_state)
        answer, error = pg.create_answer_and_error_texts()
        expected_answer = ('<bold>Water</bold> <bold>likes</bold> <bold>dogs</bold><bold>.</bold> ' +
                           '<bold>The dogs</bold> <bold>like</bold> <bold>the water</bold><bold>!</bold>' +
                           ' -- error count: 8')
        self.assertEqual(answer, expected_answer)
        self.assertEqual(error, 'Waters likes a dogs, the dog like a water,')

    def test_create_answer_and_error_paragraphs_num_paragraphs(self):
        seed(451)

        self.config_state['paragraph_size'] = 2
        self.config_state['num_paragraphs'] = 3
        pg = ParagraphsGenerator(self.config_state)
        answers, errors = pg.create_answer_and_error_paragraphs()
        expected_answers = [
            "You use <bold>a dog</bold>. The dog <bold>likes</bold> water. -- error count: 2",
            "Water uses <bold>a cat</bold>! The cat doesn't like Joe<bold>.</bold> -- error count: 2",
            "Joe likes <bold>cats</bold>. The cats don't like Bob. -- error count: 1"
        ]
        expected_errors = [
            "You use a dogs. The dog like water.",
            "Water uses cat! The cat doesn't like Joe,",
            "Joe likes cat. The cats don't like Bob."
        ]
        self.assertEqual(answers, expected_answers)
        self.assertEqual(errors, expected_errors)

        pg.update_options({'num_paragraphs': 5})
        answers, errors = pg.create_answer_and_error_paragraphs()
        self.assertEqual(len(answers), 5)
        self.assertEqual(len(errors), 5)
