import unittest

from sentences.backend.wordconnector import connect_words, flatten_paragraph, convert_paragraph, is_punctuation
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.new_word import NewNoun
from sentences.words.new_verb import NewVerb
from sentences.words.basicword import BasicWord


class TestWordConnector(unittest.TestCase):
    def test_connect_words_no_punctuation(self):
        lst = [Pronoun.I, BasicWord('like'), BasicWord('big'), BasicWord('butts')]
        self.assertEqual(connect_words(lst), 'I like big butts')

    def test_connect_words_with_punctuation(self):
        lst = [BasicWord('on').capitalize(), BasicWord('Tuesday'), Punctuation.COMMA, Pronoun.I,
               NewVerb('see', 'saw', '').past_tense(), NewNoun('A').indefinite(), Punctuation.COMMA,
               NewNoun('B').indefinite(), Punctuation.COMMA, BasicWord('and'), NewNoun('C').indefinite(),
               Punctuation.EXCLAMATION]
        self.assertEqual(connect_words(lst), "On Tuesday, I saw an A, a B, and a C!")

    def test_complex_case(self):
        lst = [Pronoun.US.subject().capitalize(), NewVerb('eat', 'ate', '').negative().past_tense(),
               NewNoun('cake').plural().capitalize().definite(), BasicWord('or'),
               NewNoun('octopus', 'octopodes').definite().plural().capitalize(), Punctuation.PERIOD]
        self.assertEqual(connect_words(lst), "We didn't eat the Cakes or The octopodes.")

    def test_flatten_paragraph(self):
        paragraph = [['some', 'words'], ['another', 'sentence'], ['a third']]
        self.assertEqual(flatten_paragraph(paragraph), ['some', 'words', 'another', 'sentence', 'a third'])

    def test_convert_paragraph(self):
        paragraph = [[Pronoun.I, BasicWord('like'), BasicWord('big'), BasicWord('butts'), Punctuation.COMMA],
                     [BasicWord('and'), Pronoun.I, BasicWord('cannot'), BasicWord('lie'), Punctuation.EXCLAMATION]]
        self.assertEqual(convert_paragraph(paragraph),
                         'I like big butts, and I cannot lie!')

    def test_convert_paragraph_bold(self):
        paragraph = [[Pronoun.I, BasicWord('like'), BasicWord('big'), BasicWord('butts'), Punctuation.COMMA],
                     [BasicWord('and'), Pronoun.I, BasicWord('cannot'), BasicWord('lie'), Punctuation.EXCLAMATION]]
        paragraph = [[word.bold() for word in sentence] for sentence in paragraph]
        self.assertEqual(
            convert_paragraph(paragraph),
            '<bold>I</bold> <bold>like</bold> <bold>big</bold> <bold>butts</bold><bold>,</bold> <bold>and</bold>' +
            ' <bold>I</bold> <bold>cannot</bold> <bold>lie</bold><bold>!</bold>'
        )

    def test_is_punctuation(self):
        punctuation = [p for p in Punctuation]
        bold_punctuation = [p.bold() for p in Punctuation]
        other = [BasicWord('.'), Pronoun.I, Pronoun.I.bold(), NewNoun('.'), NewNoun('hi').bold(),
                 NewVerb('.'), NewVerb('play').bold()]
        false_positive = BasicWord('.').bold()

        for word in punctuation:
            self.assertTrue(is_punctuation(word))
        for word in bold_punctuation:
            self.assertTrue(is_punctuation(word))
        for word in other:
            self.assertFalse(is_punctuation(word))

        self.assertTrue(is_punctuation(false_positive))
