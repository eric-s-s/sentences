import unittest

from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.punctuation import Punctuation


class TestParagraph(unittest.TestCase):
    def test_init_empty(self):
        paragraph = Paragraph([])
        self.assertEqual(paragraph.tags, Tags())
        self.assertEqual(paragraph.sentence_list(), [])

    def test_init(self):
        sentence_list = [Sentence([BasicWord('hi')]), Sentence([BasicWord('ho')])]
        tags = Tags([StatusTag.RAW])

        paragraph = Paragraph(sentence_list, tags)
        self.assertEqual(paragraph.tags, tags)
        self.assertEqual(paragraph.sentence_list(), sentence_list)
        self.assertIsNot(paragraph.tags, tags)
        self.assertIsNot(paragraph.sentence_list(), sentence_list)

        old_sentence_list = paragraph.sentence_list()
        sentence_list[0] = Sentence([BasicWord('yo')])
        self.assertEqual(paragraph.sentence_list(), old_sentence_list)
        self.assertNotEqual(paragraph.sentence_list(), sentence_list)

    def test_from_word_lists(self):
        word_lists = [[BasicWord('hi')], [BasicWord('ho')]]
        tags = Tags([StatusTag.RAW])
        paragraph = Paragraph.from_word_lists(word_lists, tags)
        self.assertEqual(paragraph.sentence_list(), [Sentence(lst) for lst in word_lists])
        self.assertEqual(paragraph.tags, tags)

        paragraph = Paragraph.from_word_lists(word_lists)
        self.assertEqual(paragraph.sentence_list(), [Sentence(lst) for lst in word_lists])
        self.assertEqual(paragraph.tags, Tags())

    def test__eq__true(self):
        sentences = [Sentence([BasicWord('a'), BasicWord('b')]),
                     Sentence([BasicWord('c')])]
        tags = Tags([StatusTag.RAW, StatusTag.GRAMMATICAL])
        self.assertEqual(Paragraph(sentences, tags), Paragraph(sentences, tags))

    def test__eq__false_by_tags(self):
        sentences = [Sentence([BasicWord('a'), BasicWord('b')]),
                     Sentence([BasicWord('c')])]
        self.assertNotEqual(Paragraph(sentences, Tags([StatusTag.GRAMMATICAL])),
                            Paragraph(sentences, Tags()))

    def test__eq__false_by_sentence_list(self):
        tags = Tags([StatusTag.GRAMMATICAL])
        self.assertNotEqual(Paragraph([Sentence([BasicWord('a')])], tags),
                            Paragraph([Sentence([BasicWord('b')])], tags))

    def test__eq__false_by_type(self):
        self.assertNotEqual(Paragraph([]), [[]])

    def test_len(self):
        sentence_list = [Sentence([BasicWord('hi')]), Sentence([BasicWord('ho')])]
        tags = Tags([StatusTag.RAW])
        paragraph = Paragraph(sentence_list, tags)
        self.assertEqual(len(paragraph), 2)

    def test_iteration(self):
        sentence_list = [Sentence([BasicWord('hi')]), Sentence([BasicWord('ho')])]
        tags = Tags([StatusTag.RAW])
        paragraph = Paragraph(sentence_list, tags)
        for index, sentence in enumerate(paragraph):
            self.assertEqual(sentence, sentence_list[index])

        self.assertTrue(sentence_list[0] in paragraph)
        self.assertFalse(Sentence([BasicWord('hope')]) in paragraph)

    def test_str(self):
        sentence_list = [Sentence([BasicWord('hi'), BasicWord('there'), Punctuation.PERIOD]),
                         Sentence([BasicWord('ho'), BasicWord('there'), Punctuation.EXCLAMATION])]
        tags = Tags([StatusTag.RAW])
        paragraph = Paragraph(sentence_list, tags)
        self.assertEqual(str(paragraph), 'hi there. ho there!')

    def test_all_words(self):
        sentence_one = [BasicWord('hi'), BasicWord('there')]
        sentence_two = [BasicWord('ho'), BasicWord('there')]
        paragraph = Paragraph([Sentence(sentence_one), Sentence(sentence_two)])
        all_words = sentence_one + sentence_two
        for index, word in enumerate(paragraph.all_words()):
            self.assertEqual(word, all_words[index])

    def test_indexed_all_words(self):
        sentence_one = [BasicWord('hi'), BasicWord('there'), BasicWord('guy')]
        sentence_two = [BasicWord('ho'), BasicWord('there')]
        paragraph = Paragraph([Sentence(sentence_one), Sentence(sentence_two)])
        all_sentences = [sentence_one, sentence_two]
        for s_index, w_index, word in paragraph.indexed_all_words():
            self.assertEqual(word, all_sentences[s_index][w_index])

    def test_set(self):
        sentences = [Sentence([BasicWord('hi'), BasicWord('there')]), Sentence([BasicWord('ho')])]
        tags = Tags([StatusTag.NOUN_ERRORS])
        paragraph = Paragraph(sentences, tags)
        new_paragraph = paragraph.set(0, 1, BasicWord('new'))

        self.assertEqual(paragraph.sentence_list(), sentences)
        self.assertEqual(paragraph.tags, tags)

        expected = [Sentence([BasicWord('hi'), BasicWord('new')]), Sentence([BasicWord('ho')])]
        self.assertEqual(new_paragraph.sentence_list(), expected)
        self.assertEqual(new_paragraph.tags, tags)

    def test_set_index_error(self):
        paragraph = Paragraph.from_word_lists([[BasicWord('test')]])
        self.assertRaises(IndexError, paragraph.set, 10, 0, BasicWord('x'))
        self.assertRaises(IndexError, paragraph.set, 0, 10, BasicWord('x'))

    def test_set_sentence(self):
        tags = Tags([StatusTag.RAW])
        sentences = [Sentence(), Sentence(), Sentence()]
        new_sentence = Sentence([BasicWord('z')])

        paragraph = Paragraph(sentences, tags).set_sentence(1, new_sentence)
        expected = Paragraph([Sentence(), new_sentence, Sentence()], tags)
        self.assertEqual(paragraph, expected)

    def test_set_tags(self):
        sentence_list = [Sentence([BasicWord('test')])]
        paragraph = Paragraph(sentence_list, Tags([StatusTag.HAS_PLURALS]))
        new = paragraph.set_tags(Tags([StatusTag.RAW]))
        self.assertEqual(new.sentence_list(), sentence_list)
        self.assertEqual(new.tags, Tags([StatusTag.RAW]))

    def test_find_word_not_present(self):
        paragraph = Paragraph.from_word_lists([[BasicWord('x')]])
        self.assertEqual(paragraph.find(BasicWord('y')), [])

    def test_find(self):
        paragraph = Paragraph.from_word_lists([
            [BasicWord('x'), BasicWord('y')],
            [BasicWord('z'), BasicWord('y'), BasicWord('x')],
            [BasicWord('q')]
        ])
        self.assertEqual(paragraph.find(BasicWord('x')), [(0, 0), (1, 2)])


if __name__ == '__main__':
    unittest.main()
