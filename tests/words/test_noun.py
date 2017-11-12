import unittest
import string

from sentences.words.noun import Noun, Word, PluralNoun, DefiniteNoun, IndefiniteNoun, DefinitePluralNoun


class TestNoun(unittest.TestCase):

    def test_noun_typing(self):
        noun = Noun('bbo')
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)

    def test_indefinite_noun_typing(self):
        noun = IndefiniteNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)

    def test_definite_noun_typing(self):
        noun = DefiniteNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)

    def test_plural_noun_typing(self):
        noun = PluralNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)

    def test_definite_plural_noun_typing(self):
        noun = DefinitePluralNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertIsInstance(noun, DefiniteNoun)
        self.assertIsInstance(noun, PluralNoun)
        self.assertIsInstance(noun, DefinitePluralNoun)

    def test_capitalize_is_still_noun(self):
        noun = Noun('dog').capitalize()
        self.assertIsInstance(noun, Noun)
        self.assertEqual(noun, Noun('Dog', base='dog'))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(Noun('hour').indefinite(), Noun('a hour', base='hour'))
        self.assertEqual(Noun('happy hour').indefinite(), Noun('a happy hour', base='happy hour'))

    def test_indefinite_vowel_start(self):
        self.assertEqual(Noun('elephant').indefinite(), Noun('an elephant', base='elephant'))
        self.assertEqual(Noun('old man').indefinite(), Noun('an old man', base='old man'))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(Noun(vowel).indefinite(), Noun('an ' + vowel, '', vowel))

    def test_indefinite_all_non_vowels(self):
        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(Noun(consonant).indefinite(), Noun('a ' + consonant, '', consonant))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').indefinite(), Noun('an octopus', 'an octopodes', 'octopus'))

    # def test_definite(self):
    #     self.assertEqual(Noun('hour').definite(), Noun('the hour'))
    #     self.assertEqual(Noun('happy hour').definite(), Noun('the happy hour'))
    #
    # def test_definite_preserves_plural(self):
    #     self.assertEqual(Noun('octopus', 'octopodes').definite(), Noun('the octopus', 'the octopodes'))
    #
    # def test_plural_no_special(self):
    #     self.assertEqual(Noun('bob').plural(), Noun('bobs'))
    #     self.assertEqual(Noun('bobo').plural(), Noun('boboes'))
    #     self.assertEqual(Noun('half').plural(), Noun('halves'))
    #     self.assertEqual(Noun('baby').plural(), Noun('babies'))
    #     self.assertEqual(Noun('ex').plural(), Noun('exes'))
    #
    # def test_plural_with_special(self):
    #     self.assertEqual(Noun('bobo', 'bobi').plural(), Noun('bobi'))
    #
    # def test_plural_does_not_pass_special_to_new_value(self):
    #     self.assertEqual(Noun('bobo', 'bobi').plural().plural(), Noun('bobis'))
    #
    # def test_eq_uses_plural_method(self):
    #     self.assertEqual(Noun('bob'), Noun('bob', 'bobs'))
    #     self.assertNotEqual(Noun('datum', 'data'), Noun('datum'))
    #
    # def test_eq_must_be_noun(self):
    #     self.assertNotEqual(Noun('bob'), Word('bob'))
    #
    # def test_indefinite_returns_indefinite_noun(self):
    #     answer = Noun('bob').indefinite()
    #     self.assertIsInstance(answer, IndefiniteNoun)
    #     self.assertEqual(answer, Noun('a bob'))
    #
    #     answer = IndefiniteNoun('a bob').indefinite()
    #     self.assertIsInstance(answer, IndefiniteNoun)
    #     self.assertEqual(answer, Noun('an a bob'))
    #
    #     answer = DefiniteNoun('the bob').indefinite()
    #     self.assertIsInstance(answer, IndefiniteNoun)
    #     self.assertEqual(answer, Noun('a the bob'))
    #
    #     answer = PluralNoun('bobs').indefinite()
    #     self.assertIsInstance(answer, IndefiniteNoun)
    #     self.assertEqual(answer, Noun('a bobs'))
    #
    #     answer = DefinitePluralNoun('the bobs').indefinite()
    #     self.assertIsInstance(answer, IndefiniteNoun)
    #     self.assertEqual(answer, Noun('a the bobs'))
    #
    # def test_definite_returns_definite_noun(self):
    #     answer = Noun('bob').definite()
    #     self.assertIsInstance(answer, DefiniteNoun)
    #     self.assertNotIsInstance(answer, PluralNoun)
    #     self.assertEqual(answer, Noun('the bob'))
    #
    #     answer = IndefiniteNoun('a bob').definite()
    #     self.assertIsInstance(answer, DefiniteNoun)
    #     self.assertNotIsInstance(answer, PluralNoun)
    #     self.assertEqual(answer, Noun('the a bob'))
    #
    #     answer = DefiniteNoun('the bob').definite()
    #     self.assertIsInstance(answer, DefiniteNoun)
    #     self.assertNotIsInstance(answer, PluralNoun)
    #     self.assertEqual(answer, Noun('the the bob'))
    #
    #     answer = PluralNoun('bobs').definite()
    #     self.assertIsInstance(answer, DefinitePluralNoun)
    #     self.assertEqual(answer, Noun('the bobs'))
    #
    #     answer = DefinitePluralNoun('the bobs').definite()
    #     self.assertIsInstance(answer, DefinitePluralNoun)
    #     self.assertEqual(answer, Noun('the the bobs'))
    #
    # def test_plural_returns_plural_noun(self):
    #     answer = Noun('bob').plural()
    #     self.assertIsInstance(answer, PluralNoun)
    #     self.assertNotIsInstance(answer, DefiniteNoun)
    #     self.assertEqual(answer, Noun('bobs'))
    #
    #     answer = IndefiniteNoun('a bob').plural()
    #     self.assertIsInstance(answer, PluralNoun)
    #     self.assertNotIsInstance(answer, DefiniteNoun)
    #     self.assertEqual(answer, Noun('a bobs'))
    #
    #     answer = DefiniteNoun('the bob').plural()
    #     self.assertIsInstance(answer, DefinitePluralNoun)
    #     self.assertEqual(answer, Noun('the bobs'))
    #
    #     answer = PluralNoun('bobs').plural()
    #     self.assertIsInstance(answer, PluralNoun)
    #     self.assertNotIsInstance(answer, DefiniteNoun)
    #     self.assertEqual(answer, Noun('bobses'))
    #
    #     answer = DefinitePluralNoun('the bobs').plural()
    #     self.assertIsInstance(answer, DefinitePluralNoun)
    #     self.assertEqual(answer, Noun('the bobses'))
