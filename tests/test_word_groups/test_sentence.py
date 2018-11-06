import unittest

from sentences.word_groups.sentence import Sentence

from sentences.words.basicword import BasicWord
from sentences.words.verb import Verb
from sentences.words.be_verb import BeVerb
from sentences.words.punctuation import Punctuation


class TestSentence(unittest.TestCase):
    def test_init_empty(self):
        sentence = Sentence()
        self.assertEqual(sentence.word_list(), [])

    def test_init_non_empty(self):
        input_list = [BasicWord('Hello'), BasicWord('world')]
        sentencce = Sentence(input_list)
        actual = sentencce.word_list()
        self.assertEqual(actual, input_list)
        self.assertIsNot(actual, input_list)

    def test_eq_true(self):
        input_list = [BasicWord('Hello'), BasicWord('world')]
        sentence = Sentence(input_list)
        other = Sentence(input_list)
        self.assertEqual(sentence, other)

    def test_eq_false_by_type(self):
        input_list = [BasicWord('hello'), BasicWord('world')]
        sentence = Sentence(input_list)
        self.assertFalse(sentence.__eq__(input_list))

    def test_eq_false_by_differing_lists(self):
        sentence = Sentence([BasicWord('I'), BasicWord('go')])
        other = Sentence([BasicWord('I'), Verb('go')])
        self.assertNotEqual(sentence, other)

    def test_sentence_str_empty(self):
        sentence = Sentence()
        self.assertEqual(str(sentence), '')

    def test_sentence_str(self):
        sentence = Sentence([BasicWord('I'), Verb('go', irregular_past='went').past_tense(), Punctuation.PERIOD])
        self.assertEqual(str(sentence), 'I went.')

    def test_sentence_str_complex_case(self):
        sentence = Sentence([
            BasicWord('He'), Verb('go').negative().third_person(), BasicWord('home'), Punctuation.COMMA,
            BasicWord('but'), BasicWord('she'), Verb('go').third_person(), BasicWord('home'), Punctuation.PERIOD
        ])
        self.assertEqual(str(sentence), "He doesn't go home, but she goes home.")

    def test_sentence_get_verb_no_verb(self):
        sentence = Sentence([BasicWord('Hello'), BasicWord('world')])
        self.assertEqual(sentence.get_verb(), -1)

    def test_sentence_get_verb_with_verb(self):
        sentence = Sentence([BasicWord('Bob'), Verb('go').third_person(), BasicWord('home')])
        self.assertEqual(sentence.get_verb(), 1)

    def test_sentence_get_verb_two_verbs_returns_first_verb(self):
        sentence = Sentence([Verb('go'), Verb('play')])
        self.assertEqual(sentence.get_verb(), 0)

    def test_sentence_get_verb_be_verb(self):
        sentence = Sentence([BasicWord('I'), BeVerb.AM.past().negative()])
        self.assertEqual(sentence.get_verb(), 1)

    def test_sentence_get_verb_returns_first_instance_of_be_verb(self):
        sentence = Sentence([BeVerb.WERE_NOT, Verb('go'), BeVerb.WERE])
        self.assertEqual(sentence.get_verb(), 0)

    def test_iteration_in_function(self):
        sentence = Sentence([BasicWord('I'), BeVerb.AM, Punctuation.PERIOD])
        self.assertTrue(BeVerb.AM in sentence)
        self.assertFalse(Punctuation.COMMA in sentence)

        self.assertIn(BasicWord('I'), sentence)
        self.assertNotIn(BeVerb.WERE, sentence)

    def test_iteration_for_loop(self):
        sentence_list = [BasicWord('I'), BeVerb.AM, Punctuation.PERIOD]
        sentence = Sentence(sentence_list)
        for index, word in enumerate(sentence):
            self.assertEqual(word, sentence_list[index])

    def test_len(self):
        sentence = Sentence([BasicWord('I'), BeVerb.AM, Punctuation.EXCLAMATION])
        self.assertEqual(len(sentence), 3)

    def test_get(self):
        sentence = Sentence([BeVerb.AM, BasicWord('I'), Punctuation.QUESTION])
        self.assertEqual(sentence.get(0), BeVerb.AM)

    def test_get_index_error(self):
        sentence = Sentence([BeVerb.AM])
        self.assertRaises(IndexError, sentence.get, 1)

    def test_set(self):
        sentence = Sentence([BasicWord('I'), BeVerb.WERE])
        new_sentence = sentence.set(1, BeVerb.AM)
        self.assertNotEqual(sentence, new_sentence)
        self.assertEqual(new_sentence, Sentence([BasicWord('I'), BeVerb.AM]))

    def test_set_index_error(self):
        sentence = Sentence([BeVerb.AM])
        self.assertRaises(IndexError, sentence.set, 2, BeVerb.IS_NOT)

    def test_delete(self):
        sentence = Sentence([BeVerb.AM, BasicWord('I'), Punctuation.QUESTION])
        new_sentence = sentence.delete(1)
        self.assertNotEqual(sentence, new_sentence)
        self.assertEqual(new_sentence, Sentence([BeVerb.AM, Punctuation.QUESTION]))

    def test_delete_index_error(self):
        sentence = Sentence([BeVerb.AM])
        self.assertRaises(IndexError, sentence.delete, 1)

    def test_insert(self):
        sentence = Sentence([BasicWord('I'), Punctuation.PERIOD])
        new_sentence = sentence.insert(1, BeVerb.AM)
        self.assertNotEqual(sentence, new_sentence)
        self.assertEqual(new_sentence, Sentence([BasicWord('I'), BeVerb.AM, Punctuation.PERIOD]))

    def test_insert_index_out_of_range(self):
        sentence = Sentence([BeVerb.AM])
        new_sentence = sentence.insert(10, BasicWord('I'))
        self.assertEqual(new_sentence, Sentence([BeVerb.AM, BasicWord('I')]))

    def test_insert_list(self):
        sentence = Sentence([BasicWord('I'), Punctuation.PERIOD])
        new_sentence = sentence.insert_list(1, [BeVerb.AM, BasicWord('happy')])
        self.assertNotEqual(sentence, new_sentence)
        self.assertEqual(new_sentence, Sentence([BasicWord('I'), BeVerb.AM, BasicWord('happy'), Punctuation.PERIOD]))

    def test_insert_list_cannot_mutate(self):
        sentence = Sentence([BasicWord('I'), Punctuation.PERIOD])
        to_insert = [BeVerb.AM, BasicWord('happy')]
        new_sentence = sentence.insert_list(1, to_insert)
        to_insert[0] = BasicWord('hello')
        self.assertEqual(new_sentence, Sentence([BasicWord('I'), BeVerb.AM, BasicWord('happy'), Punctuation.PERIOD]))

    def test_insert_list_no_index_error(self):
        sentence = Sentence([BeVerb.AM])
        new_sentence = sentence.insert_list(3, [BeVerb.AM, BasicWord('pig')])
        self.assertEqual(new_sentence, Sentence([BeVerb.AM, BeVerb.AM, BasicWord('pig')]))

    def test_sentence_get_subject_with_verb(self):
        sentence = Sentence([BasicWord('Bob'), Verb('go').third_person(), BasicWord('home')])
        self.assertEqual(sentence.get_subject(), 0)

    def test_sentence_get_subject_be_verb(self):
        sentence = Sentence([BasicWord('big'), BasicWord('guy'), BeVerb.IS])
        self.assertEqual(sentence.get_subject(), 1)

    def test_sentence_get_subject_no_verb(self):
        sentence = Sentence([BasicWord('hello'), BasicWord('world')])
        self.assertEqual(sentence.get_subject(), -1)

    def test_sentence_get_subject_no_subject(self):
        sentence = Sentence([Verb('do'), BasicWord('it')])
        self.assertEqual(sentence.get_subject(), -1)
