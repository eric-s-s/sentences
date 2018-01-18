import unittest
import string

from sentences.words.noun import (Noun, Word, PluralNoun, DefiniteNoun, IndefiniteNoun, DefinitePluralNoun,
                                  UncountableNoun, DefiniteUncountableNoun)


class TestNoun(unittest.TestCase):

    def test_noun_typing(self):
        noun = Noun('bbo')
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertNotIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_indefinite_noun_typing(self):
        noun = IndefiniteNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertNotIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_definite_noun_typing(self):
        noun = DefiniteNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertNotIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_plural_noun_typing(self):
        noun = PluralNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertNotIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_definite_plural_noun_typing(self):
        noun = DefinitePluralNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertIsInstance(noun, DefiniteNoun)
        self.assertIsInstance(noun, PluralNoun)
        self.assertIsInstance(noun, DefinitePluralNoun)
        self.assertNotIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_uncountable_noun_typing(self):
        noun = UncountableNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertNotIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertIsInstance(noun, UncountableNoun)
        self.assertNotIsInstance(noun, DefiniteUncountableNoun)

    def test_definite_uncountable_noun_typing(self):
        noun = DefiniteUncountableNoun('bbo')
        self.assertIsInstance(noun, Noun)
        self.assertNotIsInstance(noun, IndefiniteNoun)
        self.assertIsInstance(noun, DefiniteNoun)
        self.assertNotIsInstance(noun, PluralNoun)
        self.assertNotIsInstance(noun, DefinitePluralNoun)
        self.assertIsInstance(noun, UncountableNoun)
        self.assertIsInstance(noun, DefiniteUncountableNoun)

    def test_noun_values(self):
        test = Noun('a', 'b', 'c')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, 'b')
        self.assertEqual(test.base_noun, 'c')

    def test_noun_empty_values(self):
        test = Noun('a')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, '')
        self.assertEqual(test.base_noun, 'a')

    def test_capitalize_is_still_noun(self):
        noun = Noun('dog').capitalize()
        self.assertIsInstance(noun, Noun)
        self.assertEqual(noun, Noun('Dog', base='dog'))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(Noun('hour').indefinite(), IndefiniteNoun('a hour', base='hour'))
        self.assertEqual(Noun('happy hour').indefinite(), IndefiniteNoun('a happy hour', base='happy hour'))

    def test_indefinite_vowel_start(self):
        self.assertEqual(Noun('elephant').indefinite(), IndefiniteNoun('an elephant', base='elephant'))
        self.assertEqual(Noun('old man').indefinite(), IndefiniteNoun('an old man', base='old man'))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(Noun(vowel).indefinite(), IndefiniteNoun('an ' + vowel, '', vowel))

    def test_indefinite_all_non_vowels(self):
        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(Noun(consonant).indefinite(), IndefiniteNoun('a ' + consonant, '', consonant))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').indefinite(),
                         IndefiniteNoun('an octopus', 'an octopodes', 'octopus'))

    def test_definite(self):
        self.assertEqual(Noun('hour').definite(), DefiniteNoun('the hour', base='hour'))
        self.assertEqual(Noun('happy hour').definite(), DefiniteNoun('the happy hour', base='happy hour'))

    def test_definite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').definite(),
                         DefiniteNoun('the octopus', 'the octopodes', 'octopus'))

    def test_plural_no_special(self):
        self.assertEqual(Noun('bob').plural(), PluralNoun('bobs', base='bob'))
        self.assertEqual(Noun('bobo').plural(), PluralNoun('boboes', base='bobo'))
        self.assertEqual(Noun('half').plural(), PluralNoun('halves', base='half'))
        self.assertEqual(Noun('baby').plural(), PluralNoun('babies', base='baby'))
        self.assertEqual(Noun('ex').plural(), PluralNoun('exes', base='ex'))

    def test_plural_with_special(self):
        self.assertEqual(Noun('bobo', 'bobi').plural(), PluralNoun('bobi', base='bobo'))

    def test_plural_does_not_pass_special_to_new_value(self):
        self.assertEqual(Noun('bobo', 'bobi').plural().plural(), PluralNoun('bobis', base='bobo'))

    def test_eq_uses_base_method_but_not_plural(self):
        self.assertEqual(Noun('bob', 'bobolobo', base='bo'), Noun('bob', 'bobs', base='bo'))
        self.assertNotEqual(Noun('datum', base='datum'), Noun('datum', base='hoho'))

    def test_eq_must_be_noun(self):
        self.assertNotEqual(Noun('bob'), Word('bob'))

    def test_indefinite_returns_indefinite_noun(self):
        answer = Noun('bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a bob', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('an a bob', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a the bob', base='bob'))

        answer = PluralNoun('bobs', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a bobs', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a the bobs', base='bob'))

        answer = UncountableNoun('bob', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a bob', base='bob'))

        answer = DefiniteUncountableNoun('the bob', base='bob').indefinite()
        self.assertEqual(answer, IndefiniteNoun('a the bob', base='bob'))

    def test_definite_returns_definite_noun(self):
        answer = Noun('bob').definite()
        self.assertEqual(answer, DefiniteNoun('the bob', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').definite()
        self.assertEqual(answer, DefiniteNoun('the a bob', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').definite()
        self.assertEqual(answer, DefiniteNoun('the the bob', base='bob'))

        answer = PluralNoun('bobs', base='bob').definite()
        self.assertEqual(answer, DefinitePluralNoun('the bobs', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').definite()
        self.assertEqual(answer, DefinitePluralNoun('the the bobs', base='bob'))

        answer = UncountableNoun('bob', base='bob').definite()
        self.assertEqual(answer, DefiniteUncountableNoun('the bob', base='bob'))

        answer = DefiniteUncountableNoun('the bob', base='bob').definite()
        self.assertEqual(answer, DefiniteUncountableNoun('the the bob', base='bob'))

    def test_plural_returns_plural_noun(self):
        answer = Noun('bob').plural()
        self.assertEqual(answer, PluralNoun('bobs', base='bob'))

        answer = IndefiniteNoun('a bob', base='bob').plural()
        self.assertEqual(answer, PluralNoun('a bobs', base='bob'))

        answer = DefiniteNoun('the bob', base='bob').plural()
        self.assertEqual(answer, DefinitePluralNoun('the bobs', base='bob'))

        answer = PluralNoun('bobs', base='bob').plural()
        self.assertEqual(answer, PluralNoun('bobses', base='bob'))

        answer = DefinitePluralNoun('the bobs', base='bob').plural()
        self.assertEqual(answer, DefinitePluralNoun('the bobses', base='bob'))

    def test_plural_with_f_and_fe_ending_nouns(self):
        self.assertEqual(Noun('life').plural(), PluralNoun('lives', base='life'))
        self.assertEqual(Noun('waif').plural(), PluralNoun('waifs', base='waif'))
        self.assertEqual(Noun('calf').plural(), PluralNoun('calves', base='calf'))
        self.assertEqual(Noun('leaf').plural(), PluralNoun('leaves', base='leaf'))
        self.assertEqual(Noun('loaf').plural(), PluralNoun('loaves', base='loaf'))

    def test_capitalize_all(self):
        original = Noun('bob')
        basic = original.capitalize()
        self.assertEqual(basic, Noun('Bob', base='bob'))

        uncountable = UncountableNoun('bob').capitalize()
        self.assertEqual(uncountable, UncountableNoun('Bob', base='bob'))

        definite_uncountable = UncountableNoun('bob').definite().capitalize()
        self.assertEqual(definite_uncountable, DefiniteUncountableNoun('The bob', base='bob'))

        indefinite = original.indefinite().capitalize()
        self.assertEqual(indefinite, IndefiniteNoun('A bob', base='bob'))

        definite = original.definite().capitalize()
        self.assertEqual(definite, DefiniteNoun('The bob', base='bob'))

        plural = original.plural().capitalize()
        self.assertEqual(plural, PluralNoun('Bobs', base='bob'))

        definite_plural = original.definite().plural().capitalize()
        self.assertEqual(definite_plural, DefinitePluralNoun('The bobs', base='bob'))

        plural_definite = original.plural().definite().capitalize()
        self.assertEqual(plural_definite, DefinitePluralNoun('The bobs', base='bob'))

        wacky = original.plural().capitalize().definite()
        self.assertEqual(wacky, DefinitePluralNoun('the Bobs', base='bob'))

    def test_repr(self):
        self.assertEqual(repr(Noun('bob')), "Noun('bob', '', 'bob')")
        self.assertEqual(repr(IndefiniteNoun('bob')), "IndefiniteNoun('bob', '', 'bob')")
        self.assertEqual(repr(PluralNoun('bob')), "PluralNoun('bob', '', 'bob')")
        self.assertEqual(repr(DefiniteNoun('bob')), "DefiniteNoun('bob', '', 'bob')")
        self.assertEqual(repr(DefinitePluralNoun('bob')), "DefinitePluralNoun('bob', '', 'bob')")
        self.assertEqual(repr(UncountableNoun('bob')), "UncountableNoun('bob', '', 'bob')")
        self.assertEqual(repr(DefiniteUncountableNoun('bob')), "DefiniteUncountableNoun('bob', '', 'bob')")

    def test_to_base_noun_loses_plural_info(self):
        self.assertEqual(Noun('bob', 'boba').to_base_noun(), Noun('bob'))

    def test_to_base_noun_no_special_plural(self):
        original = Noun('bob')
        self.assertEqual(original.plural().to_base_noun(), original)
        self.assertEqual(original.indefinite().to_base_noun(), original)
        self.assertEqual(original.definite().to_base_noun(), original)
        self.assertEqual(original.definite().plural().to_base_noun(), original)
        self.assertEqual(original.capitalize().plural().definite().to_base_noun(), original)

    def test_to_base_noun_special_plural(self):
        original = Noun('bob', 'boberino')
        expected = Noun('bob')
        self.assertEqual(original.plural().to_base_noun(), expected)
        self.assertEqual(original.indefinite().to_base_noun(), expected)
        self.assertEqual(original.definite().to_base_noun(), expected)
        self.assertEqual(original.definite().plural().to_base_noun(), expected)
        self.assertEqual(original.capitalize().plural().definite().to_base_noun(), expected)

    def test_hash(self):
        self.assertEqual(hash(Noun('bob')), hash("hash of Noun('bob', '', 'bob')"))
        self.assertEqual(hash(DefiniteNoun('bob')), hash("hash of DefiniteNoun('bob', '', 'bob')"))
