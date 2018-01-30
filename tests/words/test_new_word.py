import unittest

from sentences.words.new_word import (NewNoun, get_plural_value, WordTypes, WordValues)
from sentences.words.word_types import WordType as wt

class TestNoun(unittest.TestCase):

    def test_get_plural_value_f_ending_non_special(self):
        self.assertEqual(get_plural_value('cuff'), 'cuffs')
        self.assertEqual(get_plural_value('waif'), 'waifs')
        self.assertEqual(get_plural_value('cuff'), 'cuffs')
        self.assertEqual(get_plural_value('reef'), 'reefs')
        self.assertEqual(get_plural_value('safe'), 'safes')

    def test_get_plural_value_f_ending_special(self):
        self.assertEqual(get_plural_value('scarf'), 'scarves')
        self.assertEqual(get_plural_value('dwarf'), 'dwarves')
        self.assertEqual(get_plural_value('half'), 'halves')
        self.assertEqual(get_plural_value('elf'), 'elves')
        self.assertEqual(get_plural_value('shelf'), 'shelves')
        self.assertEqual(get_plural_value('leaf'), 'leaves')
        self.assertEqual(get_plural_value('wolf'), 'wolves')

    def test_get_plural_value_ife_ending(self):
        self.assertEqual(get_plural_value('life'), 'lives')
        self.assertEqual(get_plural_value('wife'), 'wives')

    def test_get_plural_value_other_noun_types(self):
        self.assertEqual(get_plural_value('a dog'), 'a dogs')
        self.assertEqual(get_plural_value('the dog'), 'the dogs')
        self.assertEqual(get_plural_value('Dog'), 'Dogs')
        self.assertEqual(get_plural_value('dogs'), 'dogses')
        self.assertEqual(get_plural_value('the dogs'), 'the dogses')

    def test_noun_values(self):
        test = NewNoun('a', 'b', 'c')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, 'b')
        self.assertEqual(test.base_noun, 'c')

    def test_noun_empty_values(self):
        test = NewNoun('a')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, '')
        self.assertEqual(test.base_noun, 'a')

    def test_capitalize_is_still_noun(self):
        noun = NewNoun('dog').capitalize()
        self.assertIsInstance(noun, NewNoun)
        self.assertEqual(noun, NewNoun('Dog', base='dog'))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(NewNoun('hour').indefinite(), NewNoun('a hour', '', 'hour', WordTypes([wt.INDEFINITE])))
        self.assertEqual(NewNoun('happy hour').indefinite(),
                         NewNoun('a happy hour', '', 'happy hour', WordTypes([wt.INDEFINITE])))

    # def test_indefinite_vowel_start(self):
    #     self.assertEqual(NewNoun('elephant').indefinite(), IndefiniteNewNoun('an elephant', base='elephant'))
    #     self.assertEqual(NewNoun('old man').indefinite(), IndefiniteNewNoun('an old man', base='old man'))
    #
    # def test_indefinite_all_vowels(self):
    #     for vowel in 'aeiouAEIOU':
    #         self.assertEqual(NewNoun(vowel).indefinite(), IndefiniteNewNoun('an ' + vowel, '', vowel))
    #
    # def test_indefinite_all_non_vowels(self):
    #     vowels = 'aeiouAEIOU'
    #     for consonant in string.ascii_letters:
    #         if consonant not in vowels:
    #             self.assertEqual(NewNoun(consonant).indefinite(), IndefiniteNewNoun('a ' + consonant, '', consonant))
    #
    # def test_indefinite_preserves_plural(self):
    #     self.assertEqual(NewNoun('octopus', 'octopodes').indefinite(),
    #                      IndefiniteNewNoun('an octopus', 'octopodes', 'octopus'))
    #
    # def test_definite(self):
    #     self.assertEqual(NewNoun('hour').definite(), DefiniteNewNoun('the hour', base='hour'))
    #     self.assertEqual(NewNoun('happy hour').definite(), DefiniteNewNoun('the happy hour', base='happy hour'))
    #
    # def test_definite_preserves_plural(self):
    #     self.assertEqual(NewNoun('octopus', 'octopodes').definite(),
    #                      DefiniteNewNoun('the octopus', 'octopodes', 'octopus'))
    #
    # def test_plural_no_special(self):
    #     self.assertEqual(NewNoun('bob').plural(), PluralNewNoun('bobs', base='bob'))
    #     self.assertEqual(NewNoun('bobo').plural(), PluralNewNoun('boboes', base='bobo'))
    #     self.assertEqual(NewNoun('half').plural(), PluralNewNoun('halves', base='half'))
    #     self.assertEqual(NewNoun('baby').plural(), PluralNewNoun('babies', base='baby'))
    #     self.assertEqual(NewNoun('ex').plural(), PluralNewNoun('exes', base='ex'))
    #
    # def test_plural_with_special(self):
    #     self.assertEqual(NewNoun('bobo', 'bobi').plural(), PluralNewNoun('bobi', 'bobi', 'bobo'))
    #
    # def test_plural_does_pass_special_to_new_value(self):
    #     self.assertEqual(NewNoun('bobo', 'bobi').plural().plural(), PluralNewNoun('bobi', 'bobi', 'bobo'))
    #
    # def test_eq_uses_irregular_plural_and_base(self):
    #     self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'x', 'c'))
    #     self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'b', 'x'))
    #     self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('x', 'b', 'c'))
    #
    #     self.assertEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'b', 'c'))
    #
    # def test_eq_must_be_noun(self):
    #     self.assertNotEqual(NewNoun('bob'), Word('bob'))
    #
    # def test_indefinite_returns_indefinite_noun(self):
    #     answer = NewNoun('bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a bob', base='bob'))
    #
    #     answer = IndefiniteNewNoun('a bob', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('an a bob', base='bob'))
    #
    #     answer = DefiniteNewNoun('the bob', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a the bob', base='bob'))
    #
    #     answer = PluralNewNoun('bobs', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a bobs', base='bob'))
    #
    #     answer = DefinitePluralNewNoun('the bobs', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a the bobs', base='bob'))
    #
    #     answer = UncountableNewNoun('bob', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a bob', base='bob'))
    #
    #     answer = DefiniteUncountableNewNoun('the bob', base='bob').indefinite()
    #     self.assertEqual(answer, IndefiniteNewNoun('a the bob', base='bob'))
    #
    # def test_definite_returns_definite_noun(self):
    #     answer = NewNoun('bob').definite()
    #     self.assertEqual(answer, DefiniteNewNoun('the bob', base='bob'))
    #
    #     answer = IndefiniteNewNoun('a bob', base='bob').definite()
    #     self.assertEqual(answer, DefiniteNewNoun('the a bob', base='bob'))
    #
    #     answer = DefiniteNewNoun('the bob', base='bob').definite()
    #     self.assertEqual(answer, DefiniteNewNoun('the the bob', base='bob'))
    #
    #     answer = PluralNewNoun('bobs', base='bob').definite()
    #     self.assertEqual(answer, DefinitePluralNewNoun('the bobs', base='bob'))
    #
    #     answer = DefinitePluralNewNoun('the bobs', base='bob').definite()
    #     self.assertEqual(answer, DefinitePluralNewNoun('the the bobs', base='bob'))
    #
    #     answer = UncountableNewNoun('bob', base='bob').definite()
    #     self.assertEqual(answer, DefiniteUncountableNewNoun('the bob', base='bob'))
    #
    #     answer = DefiniteUncountableNewNoun('the bob', base='bob').definite()
    #     self.assertEqual(answer, DefiniteUncountableNewNoun('the the bob', base='bob'))
    #
    # def test_plural_returns_plural_noun(self):
    #     answer = NewNoun('bob').plural()
    #     self.assertEqual(answer, PluralNewNoun('bobs', base='bob'))
    #
    #     answer = IndefiniteNewNoun('a bob', base='bob').plural()
    #     self.assertEqual(answer, PluralNewNoun('a bobs', base='bob'))
    #
    #     answer = DefiniteNewNoun('the bob', base='bob').plural()
    #     self.assertEqual(answer, DefinitePluralNewNoun('the bobs', base='bob'))
    #
    #     answer = PluralNewNoun('bobs', base='bob').plural()
    #     self.assertEqual(answer, PluralNewNoun('bobses', base='bob'))
    #
    #     answer = DefinitePluralNewNoun('the bobs', base='bob').plural()
    #     self.assertEqual(answer, DefinitePluralNewNoun('the bobses', base='bob'))
    #
    # def test_plural_with_f_and_fe_ending_nouns(self):
    #     self.assertEqual(NewNoun('life').plural(), PluralNewNoun('lives', base='life'))
    #     self.assertEqual(NewNoun('waif').plural(), PluralNewNoun('waifs', base='waif'))
    #     self.assertEqual(NewNoun('calf').plural(), PluralNewNoun('calves', base='calf'))
    #     self.assertEqual(NewNoun('leaf').plural(), PluralNewNoun('leaves', base='leaf'))
    #
    # def test_capitalize_all(self):
    #     original = NewNoun('bob')
    #     basic = original.capitalize()
    #     self.assertEqual(basic, NewNoun('Bob', base='bob'))
    #
    #     uncountable = UncountableNewNoun('bob').capitalize()
    #     self.assertEqual(uncountable, UncountableNewNoun('Bob', base='bob'))
    #
    #     definite_uncountable = UncountableNewNoun('bob').definite().capitalize()
    #     self.assertEqual(definite_uncountable, DefiniteUncountableNewNoun('The bob', base='bob'))
    #
    #     indefinite = original.indefinite().capitalize()
    #     self.assertEqual(indefinite, IndefiniteNewNoun('A bob', base='bob'))
    #
    #     definite = original.definite().capitalize()
    #     self.assertEqual(definite, DefiniteNewNoun('The bob', base='bob'))
    #
    #     plural = original.plural().capitalize()
    #     self.assertEqual(plural, PluralNewNoun('Bobs', base='bob'))
    #
    #     definite_plural = original.definite().plural().capitalize()
    #     self.assertEqual(definite_plural, DefinitePluralNewNoun('The bobs', base='bob'))
    #
    #     plural_definite = original.plural().definite().capitalize()
    #     self.assertEqual(plural_definite, DefinitePluralNewNoun('The bobs', base='bob'))
    #
    #     wacky = original.plural().capitalize().definite()
    #     self.assertEqual(wacky, DefinitePluralNewNoun('the Bobs', base='bob'))
    #
    #     proper = ProperNewNoun('Bob')
    #     self.assertEqual(proper.capitalize(), proper)
    #
    #     proper_plural = PluralProperNewNoun('The Bobs')
    #     self.assertEqual(proper_plural.capitalize(), proper_plural)
    #
    # def test_de_capitalize_all(self):
    #     original = NewNoun('bob')
    #     basic = original.capitalize()
    #     self.assertEqual(basic.de_capitalize(), NewNoun('bob', base='bob'))
    #
    #     uncountable = UncountableNewNoun('bob').capitalize()
    #     self.assertEqual(uncountable.de_capitalize(), UncountableNewNoun('bob', base='bob'))
    #
    #     definite_uncountable = UncountableNewNoun('bob').definite().capitalize()
    #     self.assertEqual(definite_uncountable.de_capitalize(), DefiniteUncountableNewNoun('the bob', base='bob'))
    #
    #     indefinite = original.indefinite().capitalize()
    #     self.assertEqual(indefinite.de_capitalize(), IndefiniteNewNoun('a bob', base='bob'))
    #
    #     definite = original.definite().capitalize()
    #     self.assertEqual(definite.de_capitalize(), DefiniteNewNoun('the bob', base='bob'))
    #
    #     plural = original.plural().capitalize()
    #     self.assertEqual(plural.de_capitalize(), PluralNewNoun('bobs', base='bob'))
    #
    #     definite_plural = original.definite().plural().capitalize()
    #     self.assertEqual(definite_plural.de_capitalize(), DefinitePluralNewNoun('the bobs', base='bob'))
    #
    #     plural_definite = original.plural().definite().capitalize()
    #     self.assertEqual(plural_definite.de_capitalize(), DefinitePluralNewNoun('the bobs', base='bob'))
    #
    #     wacky = original.plural().capitalize().definite()
    #     self.assertEqual(wacky.de_capitalize(), DefinitePluralNewNoun('the Bobs', base='bob'))
    #
    #     proper = ProperNewNoun('Bob').de_capitalize()
    #     self.assertEqual(ProperNewNoun('Bob', '', 'Bob'), proper)
    #
    #     proper_plural = PluralProperNewNoun('The Bobs').de_capitalize()
    #     self.assertEqual(PluralProperNewNoun('The Bobs', '', 'The Bobs'), proper_plural)
    #
    # def test_repr(self):
    #     self.assertEqual(repr(NewNoun('bob')), "NewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(IndefiniteNewNoun('bob')), "IndefiniteNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(PluralNewNoun('bob')), "PluralNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(DefiniteNewNoun('bob')), "DefiniteNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(DefinitePluralNewNoun('bob')), "DefinitePluralNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(UncountableNewNoun('bob')), "UncountableNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(DefiniteUncountableNewNoun('bob')), "DefiniteUncountableNewNoun('bob', '', 'bob')")
    #     self.assertEqual(repr(ProperNewNoun('Bob')), "ProperNewNoun('Bob', '', 'Bob')")
    #     self.assertEqual(repr(PluralProperNewNoun('Bobs')), "PluralProperNewNoun('Bobs', '', 'Bobs')")
    #
    # def test_to_base_noun_keeps_plural_info(self):
    #     self.assertEqual(NewNoun('bob', 'boba').to_base_noun(), NewNoun('bob', 'boba'))
    #
    # def test_to_base_noun_no_special_plural(self):
    #     original = NewNoun('bob')
    #     self.assertEqual(original.plural().to_base_noun(), original)
    #     self.assertEqual(original.indefinite().to_base_noun(), original)
    #     self.assertEqual(original.definite().to_base_noun(), original)
    #     self.assertEqual(original.definite().plural().to_base_noun(), original)
    #     self.assertEqual(original.capitalize().plural().definite().to_base_noun(), original)
    #
    # def test_to_base_noun_special_plural(self):
    #     original = NewNoun('bob', 'boberino')
    #     expected = NewNoun('bob', 'boberino')
    #     self.assertEqual(original.plural().to_base_noun(), expected)
    #     self.assertEqual(original.indefinite().to_base_noun(), expected)
    #     self.assertEqual(original.definite().to_base_noun(), expected)
    #     self.assertEqual(original.definite().plural().to_base_noun(), expected)
    #     self.assertEqual(original.capitalize().plural().definite().to_base_noun(), expected)
    #
    # def test_hash(self):
    #     self.assertEqual(hash(NewNoun('bob')), hash("hash of NewNoun('bob', '', 'bob')"))
    #     self.assertEqual(hash(DefiniteNewNoun('bob')), hash("hash of DefiniteNewNoun('bob', '', 'bob')"))
    #
    # def test_indefinite_plural(self):
    #     noun = NewNoun('dog')
    #     new = noun.indefinite().plural()
    #     self.assertEqual(new, PluralNewNoun('a dogs', '', 'dog'))
    #
    #     irregular = NewNoun('child', 'children')
    #     new = irregular.indefinite().plural()
    #     self.assertEqual(new, PluralNewNoun('a children', 'children', 'child'))
    #
    # def test_plural_indefinite(self):
    #     noun = NewNoun('dog')
    #     new = noun.plural().indefinite()
    #     self.assertEqual(new, IndefiniteNewNoun('a dogs', '', 'dog'))
    #
    #     irregular = NewNoun('child', 'children')
    #     new = irregular.plural().indefinite()
    #     self.assertEqual(new, IndefiniteNewNoun('a children', 'children', 'child'))
    #
    # def test_uncountable_plural(self):
    #     noun = UncountableNewNoun('water')
    #     self.assertEqual(noun.plural(), PluralNewNoun('waters', '', 'water'))
    #
    # def test_definite_uncountable_plural(self):
    #     noun = UncountableNewNoun('water')
    #     self.assertEqual(noun.definite().plural(), DefinitePluralNewNoun('the waters', '', 'water'))
    #
    # def test_proper_noun_plural(self):
    #     noun = ProperNewNoun('Bob')
    #     self.assertEqual(noun.plural(), PluralProperNewNoun('Bobs', '', 'Bob'))
    #
    # def test_plural_proper_noun_plural(self):
    #     noun = PluralProperNewNoun('Bobs', '', 'Bob')
    #     self.assertEqual(noun.plural(), noun)
    #
    # def test_proper_noun_ignores_irregular(self):
    #     noun = ProperNewNoun('The Magus', 'The Magi')
    #     self.assertEqual(noun.plural(), PluralProperNewNoun('The Maguses', 'The Magi', 'The Magus'))
    #
    # def test_proper_noun_definite(self):
    #     noun = ProperNewNoun('Bob').definite()
    #     self.assertEqual(noun, DefiniteNewNoun('the Bob', '', 'Bob'))
    #
    #     noun = PluralProperNewNoun('Bobs').definite()
    #     self.assertEqual(noun, DefinitePluralNewNoun('the Bobs', '', 'Bobs'))
    #
    # def test_proper_noun_definite_and_plural(self):
    #     noun = ProperNewNoun('Bob').plural().definite()
    #     self.assertEqual(noun, DefinitePluralNewNoun('the Bobs', '', 'Bob'))
    #
    #     noun = ProperNewNoun('Bob').definite().plural()
    #     self.assertEqual(noun, DefinitePluralNewNoun('the Bobs', '', 'Bob'))
    #
    # def test_proper_noun_indefinite_an(self):
    #     noun = ProperNewNoun('Ed')
    #     plural = noun.plural()
    #
    #     self.assertEqual(noun.indefinite(), IndefiniteNewNoun('an Ed', '', 'Ed'))
    #     self.assertEqual(plural.indefinite(), IndefiniteNewNoun('an Eds', '', 'Ed'))
    #
    # def test_proper_noun_capitalize(self):
    #     noun = ProperNewNoun('Ed')
    #     plural = noun.plural()
    #
    #     self.assertEqual(noun.capitalize(), noun)
    #     self.assertEqual(plural.capitalize(), plural)
    #
    #     sports_team = PluralProperNewNoun('the Guys')
    #     self.assertEqual(sports_team.capitalize(), PluralProperNewNoun('The Guys', '', 'the Guys'))
    #
    # def test_proper_noun_de_capitalize_starts_with_capital(self):
    #     noun = ProperNewNoun('Joe')
    #     plural = noun.plural()
    #
    #     self.assertEqual(noun.de_capitalize(), noun)
    #     self.assertEqual(plural.de_capitalize(), plural)
    #
    # def test_proper_noun_de_capitalize_starts_with_lower_case(self):
    #     noun = ProperNewNoun('the Dude')
    #     plural = noun.plural()
    #     capital_noun = noun.capitalize()
    #     capital_plural = plural.capitalize()
    #
    #     self.assertEqual(noun.de_capitalize(), noun)
    #     self.assertEqual(capital_noun.de_capitalize(), noun)
    #     self.assertEqual(plural.de_capitalize(), plural)
    #     self.assertEqual(capital_plural.de_capitalize(), plural)
