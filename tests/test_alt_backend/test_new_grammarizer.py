import unittest

from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.tags.status_tag import StatusTag
from sentences.tags.tags import Tags
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.basicword import BasicWord
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun
from sentences.words.verb import Verb


class TestNewGrammarizer(unittest.TestCase):
    def test_init(self):
        paragraph = Paragraph([Sentence([Noun('x')])], Tags([StatusTag.RAW]))
        grammarizer = NewGrammarizer(paragraph)
        self.assertEqual(grammarizer.raw.sentence_list(), paragraph.sentence_list())
        self.assertEqual(grammarizer.raw.tags, Tags([StatusTag.RAW]))

    def test_grammarize_to_present_or_past_tense_changes_tags(self):
        tags = Tags([StatusTag.RAW, StatusTag.HAS_PLURALS, StatusTag.HAS_NEGATIVES])
        paragraph = Paragraph([Sentence([Noun('x')])], tags)
        grammarizer = NewGrammarizer(paragraph)
        new_paragraph = grammarizer.grammarize_to_present_tense()
        self.assertEqual(new_paragraph.tags, tags.remove(StatusTag.RAW).add(StatusTag.GRAMMATICAL))

        new_paragraph = grammarizer.grammarize_to_past_tense()
        self.assertEqual(new_paragraph.tags, tags.remove(StatusTag.RAW).add(StatusTag.GRAMMATICAL))

    def test_grammarize_to_present_or_past_tense_gives_singular_nouns_proper_articles(self):
        base_word_list = [Noun('x'), BasicWord('x')]
        indefinite_word_list = [Noun('x').indefinite(), BasicWord('x')]
        definite_word_list = [Noun('x').definite(), BasicWord('x')]
        expected = [Sentence(indefinite_word_list)] + [Sentence(definite_word_list) for _ in range(2)]

        raw_paragraph = Paragraph([Sentence(base_word_list) for _ in range(3)])

        new_past = NewGrammarizer(raw_paragraph).grammarize_to_past_tense()
        new_present = NewGrammarizer(raw_paragraph).grammarize_to_present_tense()

        self.assertEqual(new_past.sentence_list(), expected)
        self.assertEqual(new_present.sentence_list(), expected)

    def test_grammarize_to_present_or_past_tense_gives_plural_nouns_proper_articles(self):
        base_word_list = [Noun('x').plural(), BasicWord('x')]
        indefinite_word_list = [Noun('x').plural(), BasicWord('x')]
        definite_word_list = [Noun('x').definite().plural(), BasicWord('x')]
        expected = [Sentence(indefinite_word_list)] + [Sentence(definite_word_list) for _ in range(2)]

        raw_paragraph = Paragraph([Sentence(base_word_list) for _ in range(3)])

        new_past = NewGrammarizer(raw_paragraph).grammarize_to_past_tense()
        new_present = NewGrammarizer(raw_paragraph).grammarize_to_present_tense()

        self.assertEqual(new_past.sentence_list(), expected)
        self.assertEqual(new_present.sentence_list(), expected)

    def test_grammarize_to_present_or_past_tense_does_not_alter_proper_nouns_or_uncountable_nouns(self):
        word_list = [Noun.proper_noun('x', plural=True),
                     Noun.proper_noun('y', plural=False),
                     Noun.uncountable_noun('z')]
        sentence_list = [Sentence(word_list) for _ in range(3)]
        raw_paragraph = Paragraph(sentence_list)

        new_past = NewGrammarizer(raw_paragraph).grammarize_to_past_tense()
        new_present = NewGrammarizer(raw_paragraph).grammarize_to_present_tense()

        self.assertEqual(new_past.sentence_list(), sentence_list)
        self.assertEqual(new_present.sentence_list(), sentence_list)

    def test_grammarize_to_present_tense_makes_verb_third_person_when_subject_is_singular_noun(self):
        singular_subject_sentences = [Sentence([Noun('x'), Verb('y')]),
                                      Sentence([Noun.uncountable_noun('x'), Verb('y')]),
                                      Sentence([Noun.proper_noun('x'), Verb('y').negative()])]
        new_paragraph = NewGrammarizer(Paragraph(singular_subject_sentences)).grammarize_to_present_tense()

        expected = [Sentence([Noun('x').indefinite(), Verb('y').third_person()]),
                    Sentence([Noun.uncountable_noun('x'), Verb('y').third_person()]),
                    Sentence([Noun.proper_noun('x'), Verb('y').third_person().negative()])]
        self.assertEqual(new_paragraph.sentence_list(), expected)

    def test_grammarize_to_present_tense_does_not_alter_verb_when_subject_is_plural_noun(self):
        expected = plural_subject_sentences = [Sentence([Noun('x').plural(), Verb('y').negative()]),
                                               Sentence([Noun.proper_noun('x', plural=True), Verb('y')])]

        new_paragraph = NewGrammarizer(Paragraph(plural_subject_sentences)).grammarize_to_present_tense()
        self.assertEqual(new_paragraph.sentence_list(), expected)

    def test_grammarize_to_present_tense_makes_verb_third_person_when_subject_is_HE_SHE_IT(self):
        third_person_sentences = [Sentence([Pronoun.HE, Verb('x')]),
                                  Sentence([Pronoun.SHE, Verb('x').negative()]),
                                  Sentence([Pronoun.IT, Verb('x')])]
        raw_paragraph = Paragraph(third_person_sentences)
        new_paragraph = NewGrammarizer(raw_paragraph).grammarize_to_present_tense()
        expected = [Sentence([Pronoun.HE, Verb('x').third_person()]),
                    Sentence([Pronoun.SHE, Verb('x').third_person().negative()]),
                    Sentence([Pronoun.IT, Verb('x').third_person()])]
        self.assertEqual(new_paragraph.sentence_list(), expected)

    def test_grammarize_to_present_tense_does_not_alter_verb_when_subject_is_I_YOU_WE_THEY(self):
        expected = sentences = [Sentence([Pronoun.I, Verb('x')]),
                                Sentence([Pronoun.YOU, Verb('x')]),
                                Sentence([Pronoun.WE, Verb('x')]),
                                Sentence([Pronoun.THEY, Verb('x')])]
        raw_paragraph = Paragraph(sentences)
        new_paragraph = NewGrammarizer(raw_paragraph).grammarize_to_present_tense()
        self.assertEqual(new_paragraph.sentence_list(), expected)
