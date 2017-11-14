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

    def test_definite(self):
        self.assertEqual(Noun('hour').definite(), Noun('the hour', base='hour'))
        self.assertEqual(Noun('happy hour').definite(), Noun('the happy hour', base='happy hour'))

    def test_definite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').definite(), Noun('the octopus', 'the octopodes', 'octopus'))

    def test_plural_no_special(self):
        self.assertEqual(Noun('bob').plural(), Noun('bobs', base='bob'))
        self.assertEqual(Noun('bobo').plural(), Noun('boboes', base='bobo'))
        self.assertEqual(Noun('half').plural(), Noun('halves', base='half'))
        self.assertEqual(Noun('baby').plural(), Noun('babies', base='baby'))
        self.assertEqual(Noun('ex').plural(), Noun('exes', base='ex'))

    def test_plural_with_special(self):
        self.assertEqual(Noun('bobo', 'bobi').plural(), Noun('bobi', base='bobo'))

    def test_plural_does_not_pass_special_to_new_value(self):
        self.assertEqual(Noun('bobo', 'bobi').plural().plural(), Noun('bobis', base='bobo'))

    def test_eq_uses_base_method_but_not_plural(self):
        self.assertEqual(Noun('bob', 'bobolobo', base='bo'), Noun('bob', 'bobs', base='bo'))
        self.assertNotEqual(Noun('datum', base='datum'), Noun('datum', base='hoho'))

    def test_eq_must_be_noun(self):
        self.assertNotEqual(Noun('bob'), Word('bob'))

    def test_indefinite_returns_indefinite_noun(self):
        answer = Noun('bob').indefinite()
        self.assertIsInstance(answer, IndefiniteNoun)
        self.assertEqual(answer, Noun('a bob', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').indefinite()
        self.assertIsInstance(answer, IndefiniteNoun)
        self.assertEqual(answer, Noun('an a bob', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').indefinite()
        self.assertIsInstance(answer, IndefiniteNoun)
        self.assertEqual(answer, Noun('a the bob', base='bob'))

        answer = PluralNoun('bobs', base='bob').indefinite()
        self.assertIsInstance(answer, IndefiniteNoun)
        self.assertEqual(answer, Noun('a bobs', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').indefinite()
        self.assertIsInstance(answer, IndefiniteNoun)
        self.assertEqual(answer, Noun('a the bobs', base='bob'))

    def test_definite_returns_definite_noun(self):
        answer = Noun('bob').definite()
        self.assertIsInstance(answer, DefiniteNoun)
        self.assertNotIsInstance(answer, PluralNoun)
        self.assertEqual(answer, Noun('the bob', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').definite()
        self.assertIsInstance(answer, DefiniteNoun)
        self.assertNotIsInstance(answer, PluralNoun)
        self.assertEqual(answer, Noun('the a bob', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').definite()
        self.assertIsInstance(answer, DefiniteNoun)
        self.assertNotIsInstance(answer, PluralNoun)
        self.assertEqual(answer, Noun('the the bob', base='bob'))

        answer = PluralNoun('bobs', base='bob').definite()
        self.assertIsInstance(answer, DefinitePluralNoun)
        self.assertEqual(answer, Noun('the bobs', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').definite()
        self.assertIsInstance(answer, DefinitePluralNoun)
        self.assertEqual(answer, Noun('the the bobs', base='bob'))

    def test_plural_returns_plural_noun(self):
        answer = Noun('bob').plural()
        self.assertIsInstance(answer, PluralNoun)
        self.assertNotIsInstance(answer, DefiniteNoun)
        self.assertEqual(answer, Noun('bobs', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').plural()
        self.assertIsInstance(answer, PluralNoun)
        self.assertNotIsInstance(answer, DefiniteNoun)
        self.assertEqual(answer, Noun('a bobs', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').plural()
        self.assertIsInstance(answer, DefinitePluralNoun)
        self.assertEqual(answer, Noun('the bobs', base='bob'))

        answer = PluralNoun('bobs', base='bob').plural()
        self.assertIsInstance(answer, PluralNoun)
        self.assertNotIsInstance(answer, DefiniteNoun)
        self.assertEqual(answer, Noun('bobses', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').plural()
        self.assertIsInstance(answer, DefinitePluralNoun)
        self.assertEqual(answer, Noun('the bobses', base='bob'))

    def test_plural_with_f_and_fe_ending_nouns(self):
        self.assertEqual(Noun('life').plural(), Noun('lives', base='life'))
        self.assertEqual(Noun('waif').plural(), Noun('waifs', base='waif'))
        self.assertEqual(Noun('calf').plural(), Noun('calves', base='calf'))

    def test_capitalize_all(self):
        original = Noun('bob')
        basic = original.capitalize()
        self.assertEqual(basic, Noun('Bob', base='bob'))
        indefinite = original.indefinite().capitalize()
        self.assertEqual(indefinite, Noun('A bob', base='bob'))
        definite = original.definite().capitalize()
        self.assertEqual(definite, Noun('The bob', base='bob'))
        plural = original.plural().capitalize()
        self.assertEqual(plural, Noun('Bobs', base='bob'))
        definite_plural = original.definite().plural().capitalize()
        self.assertEqual(definite_plural, Noun('The bobs', base='bob'))
        plural_definite = original.plural().definite().capitalize()
        self.assertEqual(plural_definite, Noun('The bobs', base='bob'))

        wacky = original.plural().capitalize().definite()
        self.assertEqual(wacky, Noun('the Bobs', base='bob'))

    def test_repr(self):
        self.assertEqual(repr(Noun('bob')), "Noun('bob', '', 'bob')")
        self.assertEqual(repr(IndefiniteNoun('bob')), "IndefiniteNoun('bob', '', 'bob')")
        self.assertEqual(repr(PluralNoun('bob')), "PluralNoun('bob', '', 'bob')")
        self.assertEqual(repr(DefiniteNoun('bob')), "DefiniteNoun('bob', '', 'bob')")
        self.assertEqual(repr(DefinitePluralNoun('bob')), "DefinitePluralNoun('bob', '', 'bob')")

    def test_revert_loses_plural_info(self):
        self.assertEqual(Noun('bob', 'boba').revert(), Noun('bob'))

    def test_revert_no_special_plural(self):
        original = Noun('bob')
        self.assertEqual(original.plural().revert(), original)
        self.assertEqual(original.indefinite().revert(), original)
        self.assertEqual(original.definite().revert(), original)
        self.assertEqual(original.definite().plural().revert(), original)
        self.assertEqual(original.capitalize().plural().definite().revert(), original)

    def test_revert_special_plural(self):
        original = Noun('bob', 'boberino')
        expected = Noun('bob')
        self.assertEqual(original.plural().revert(), expected)
        self.assertEqual(original.indefinite().revert(), expected)
        self.assertEqual(original.definite().revert(), expected)
        self.assertEqual(original.definite().plural().revert(), expected)
        self.assertEqual(original.capitalize().plural().definite().revert(), expected)

    def test_hash(self):
        self.assertEqual(hash(Noun('bob')), hash("hash of Noun('bob', '', 'bob')"))
