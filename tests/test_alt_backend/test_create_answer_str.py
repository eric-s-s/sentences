import unittest

from sentences.alt_backend.create_answer_str import create_answer_str
from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.backend.random_assignments.assign_random_negatives import assign_random_negatives
from sentences.backend.random_assignments.plurals_assignement import PluralsAssignment
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.punctuation import Punctuation
from sentences.words.verb import Verb


class TestAnswerMaker(unittest.TestCase):
    def test_create_answer_str_makes_grammatically_correct_paragraph_if_base_paragraph_word_order_is_ok(self):
        base_sentences = [Sentence([Pronoun.HE, Verb('like'), Noun('dog'), Punctuation.PERIOD]),
                          Sentence([Noun('dog'), Verb('go'), BasicWord.preposition('to'), Noun('house'),
                                    Punctuation.PERIOD])]
        base_paragraph = Paragraph(base_sentences)
        answer = create_answer_str('', base_paragraph)
        expected = 'He likes a dog. The dog goes to a house.'
        self.assertEqual(answer, expected)

    def test_create_answer_str_makes_paragraph_according_to_plurals_in_paragraph_str(self):
        base_sentences = [Sentence([Noun('dog'), Verb('like'), Noun('cat'), Punctuation.PERIOD])]
        base_paragraph = Paragraph(base_sentences)
        paragaph_str = 'A dog like cats,'
        answer = create_answer_str(paragaph_str, base_paragraph)
        expected = 'A dog likes cats.'
        self.assertEqual(answer, expected)

    def test_create_answer_str_picks_plural_when_plural_and_singular_present(self):
        base_sentences = [Sentence([Noun('dog'), Verb('like'), Noun('dog'), Punctuation.PERIOD])]
        base_paragraph = Paragraph(base_sentences)
        for paragraph_Str in ('dogs like a dog.', 'a dog like dogs.'):
            answer = create_answer_str(paragraph_Str, base_paragraph)
            self.assertEqual(answer, 'Dogs like the dogs.')

    def test_create_answer_str_uses_base_paragraph_for_word_order_and_punctuation(self):
        base_sentences = [
            Sentence([Noun('dog'), Verb('play'), BasicWord.preposition('with'), Noun('dog'), Punctuation.PERIOD])]
        base_paragraph = Paragraph(base_sentences)
        combinations = ('dog dog with play', 'dog dog play with', 'dog with dog play', 'dog with play dog',
                        'play with dog dog', 'play dog with dog', 'with dog play dog')
        for paragraph_str in combinations:
            answer = create_answer_str(paragraph_str, base_paragraph)
            self.assertEqual(answer, 'A dog plays with the dog.')

    def test_create_answer_str_is_in_past_tense_if_has_tag_simple_past(self):
        base_sentences = [Sentence([Noun('dog'), Verb('like'), Noun('cat'), Punctuation.PERIOD])]
        base_paragraph = Paragraph(base_sentences, Tags([StatusTag.SIMPLE_PAST]))
        paragaph_str = 'A dog liked cats,'
        answer = create_answer_str(paragaph_str, base_paragraph)
        expected = 'A dog liked cats.'
        self.assertEqual(answer, expected)

    def test_create_answer_str_fully_formed_paragraph_with_different_plurals_assignment_present_tense(self):
        base_sentences = [Sentence([Noun('dog'), Verb('like'), Noun('cat'), Punctuation.PERIOD])]
        paragraph = Paragraph(base_sentences)
        new_paragraph = PluralsAssignment(assign_random_negatives(paragraph, 1.0)).assign_random_plurals(1.0)
        grammatical = NewGrammarizer(new_paragraph).grammarize_to_present_tense()

        self.assertEqual(str(grammatical), "Dogs don't like cats.")

        paragraph_str = "dog cat"
        answer = create_answer_str(paragraph_str, grammatical)
        self.assertEqual(answer, "A dog doesn't like a cat.")

    def test_create_answer_str_fully_formed_paragraph_with_different_plurals_assignment_past_tense(self):
        base_sentences = [Sentence([Noun('dog'), Verb('like'), Noun('cat'), Punctuation.PERIOD])]
        paragraph = Paragraph(base_sentences)
        new_paragraph = PluralsAssignment(assign_random_negatives(paragraph, 1.0)).assign_random_plurals(1.0)
        grammatical = NewGrammarizer(new_paragraph).grammarize_to_past_tense()

        self.assertEqual(str(grammatical), "Dogs didn't like cats.")

        paragraph_str = "dog cat"
        answer = create_answer_str(paragraph_str, grammatical)
        self.assertEqual(answer, "A dog didn't like a cat.")
