import unittest
import string

from sentences.words.noun import Noun, Word


class TestNoun(unittest.TestCase):
    def test_capitalize_is_still_noun(self):
        noun = Noun('dog').capitalize()
        self.assertIsInstance(noun, Noun)
        self.assertEqual(noun, Noun('Dog'))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(Noun('hour').indefinite(), Noun('a hour'))
        self.assertEqual(Noun('happy hour').indefinite(), Noun('a happy hour'))

    def test_indefinite_vowel_start(self):
        self.assertEqual(Noun('elephant').indefinite(), Noun('an elephant'))
        self.assertEqual(Noun('old man').indefinite(), Noun('an old man'))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(Noun(vowel).indefinite(), Noun('an ' + vowel))

    def test_indefinite_all_non_vowels(self):
        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(Noun(consonant).indefinite(), Noun('a ' + consonant))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').indefinite(), Noun('an octopus', 'an octopodes'))

    def test_definite(self):
        self.assertEqual(Noun('hour').definite(), Noun('the hour'))
        self.assertEqual(Noun('happy hour').definite(), Noun('the happy hour'))

    def test_definite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').definite(), Noun('the octopus', 'the octopodes'))

    def test_plural_no_special(self):
        self.assertEqual(Noun('bob').plural(), Noun('bobs'))
        self.assertEqual(Noun('bobo').plural(), Noun('boboes'))
        self.assertEqual(Noun('half').plural(), Noun('halves'))
        self.assertEqual(Noun('baby').plural(), Noun('babies'))
        self.assertEqual(Noun('ex').plural(), Noun('exes'))

    def test_plural_with_special(self):
        self.assertEqual(Noun('bobo', 'bobi').plural(), Noun('bobi'))

    def test_plural_does_not_pass_special_to_new_value(self):
        self.assertEqual(Noun('bobo', 'bobi').plural().plural(), Noun('bobis'))

    def test_eq_uses_plural_method(self):
        self.assertEqual(Noun('bob'), Noun('bob', 'bobs'))
        self.assertNotEqual(Noun('datum', 'data'), Noun('datum'))

    def test_eq_must_be_noun(self):
        self.assertNotEqual(Noun('bob'), Word('bob'))
