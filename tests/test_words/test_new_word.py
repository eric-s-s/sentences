import string
import unittest

from sentences.words.new_word import (NewNoun, get_plural_value, Tags)
from sentences.words.word import Word
from sentences.words.wordtools.wordtag import WordTag as wt


class TestNoun(unittest.TestCase):

    def setUp(self):
        self.indefinite = Tags([wt.INDEFINITE])
        self.definite = Tags([wt.DEFINITE])
        self.plural = Tags([wt.PLURAL])
        self.definite_plural = Tags([wt.DEFINITE, wt.PLURAL])
        self.definite_uncountable = Tags([wt.DEFINITE, wt.UNCOUNTABLE])
        self.proper = Tags([wt.PROPER])
        self.plural_proper = Tags([wt.PLURAL, wt.PROPER])

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
        self.assertEqual(noun, NewNoun('Dog', '', 'dog'))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(NewNoun('hour').indefinite(), NewNoun('a hour', '', 'hour', self.indefinite))
        self.assertEqual(NewNoun('happy hour').indefinite(),
                         NewNoun('a happy hour', '', 'happy hour', self.indefinite))

    def test_indefinite_vowel_start(self):
        self.assertEqual(NewNoun('elephant').indefinite(), NewNoun('an elephant', '', 'elephant', self.indefinite))
        self.assertEqual(NewNoun('old man').indefinite(), NewNoun('an old man', '', 'old man', self.indefinite))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(NewNoun(vowel).indefinite(), NewNoun('an ' + vowel, '', vowel, self.indefinite))

    def test_indefinite_all_non_vowels(self):

        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(NewNoun(consonant).indefinite(), NewNoun('a ' + consonant, '', consonant,
                                                                          self.indefinite))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(NewNoun('octopus', 'octopodes').indefinite(),
                         NewNoun('an octopus', 'octopodes', 'octopus', self.indefinite))

    def test_definite(self):
        self.assertEqual(NewNoun('hour').definite(), NewNoun('the hour', '', 'hour', self.definite))
        self.assertEqual(NewNoun('happy hour').definite(), NewNoun('the happy hour',  '', 'happy hour', self.definite))

    def test_definite_preserves_plural(self):
        self.assertEqual(NewNoun('octopus', 'octopodes').definite(),
                         NewNoun('the octopus', 'octopodes', 'octopus', self.definite))

    def test_plural_no_special(self):
        self.assertEqual(NewNoun('bob').plural(), NewNoun('bobs', '', 'bob', self.plural))
        self.assertEqual(NewNoun('bobo').plural(), NewNoun('boboes', '', 'bobo', self.plural))
        self.assertEqual(NewNoun('half').plural(), NewNoun('halves', '', 'half', self.plural))
        self.assertEqual(NewNoun('baby').plural(), NewNoun('babies', '', 'baby', self.plural))
        self.assertEqual(NewNoun('ex').plural(), NewNoun('exes', '', 'ex', self.plural))

    def test_plural_with_special(self):
        self.assertEqual(NewNoun('bobo', 'bobi').plural(), NewNoun('bobi', 'bobi', 'bobo', self.plural))

    def test_plural_does_pass_special_to_new_value(self):
        self.assertEqual(NewNoun('bobo', 'bobi').plural().plural(), NewNoun('bobi', 'bobi', 'bobo', self.plural))

    def test_eq_uses_irregular_plural_and_base(self):
        self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'x', 'c'))
        self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'b', 'x'))
        self.assertNotEqual(NewNoun('a', 'b', 'c'), NewNoun('x', 'b', 'c'))

        self.assertEqual(NewNoun('a', 'b', 'c'), NewNoun('a', 'b', 'c'))

    def test_eq_must_be_noun(self):
        self.assertNotEqual(NewNoun('bob'), Word('bob'))

    def test_indefinite_returns_indefinite_noun(self):
        answer = NewNoun('bob').indefinite()
        self.assertEqual(answer, NewNoun('a bob', '', 'bob', self.indefinite))

        answer = NewNoun('a bob', '', 'bob', self.indefinite).indefinite()  # TODO yes or no?
        self.assertEqual(answer, NewNoun('a bob', '', 'bob', self.indefinite))

        answer = NewNoun('the bob', '', 'bob', self.definite).indefinite()
        self.assertEqual(answer, NewNoun('a the bob', '', 'bob', self.indefinite))

        answer = NewNoun('bobs', '', 'bob', self.plural).indefinite()
        self.assertEqual(answer, NewNoun('a bobs', '', 'bob', self.indefinite))

        answer = NewNoun('the bobs', '', 'bob', self.definite_plural).indefinite()
        self.assertEqual(answer, NewNoun('a the bobs', '', 'bob', self.indefinite))

        answer = NewNoun.uncountable_noun('bob').indefinite()
        self.assertEqual(answer, NewNoun('a bob', '', 'bob', self.indefinite))

        answer = NewNoun.uncountable_noun('bob').definite().indefinite()
        self.assertEqual(answer, NewNoun('a the bob', '', 'bob', self.indefinite))

    def test_definite_returns_definite_noun(self):
        answer = NewNoun('bob').definite()
        self.assertEqual(answer, NewNoun('the bob', '', 'bob', self.definite))

        answer = NewNoun('a bob', '', 'bob', self.indefinite).definite()
        self.assertEqual(answer, NewNoun('the a bob', '', 'bob', self.definite))

        answer = NewNoun('the bob', '', 'bob', self.definite).definite()  # TODO yes or no?
        self.assertEqual(answer, NewNoun('the bob', '', 'bob', self.definite))

        answer = NewNoun('bobs', '', 'bob', self.plural).definite()
        self.assertEqual(answer, NewNoun('the bobs', '', 'bob', self.definite_plural))

        # answer = NewNoun('the bobs', '', 'bob', self.definite_plural).definite()
        # self.assertEqual(answer, NewNoun('the the bobs', '', 'bob', self.definite_plural))

        answer = NewNoun.uncountable_noun('bob').definite()
        self.assertEqual(answer, NewNoun('the bob', '', 'bob', self.definite_uncountable))

        # answer = NewNoun('the bob', '', 'bob', self.definite_uncountable).definite()
        # self.assertEqual(answer, NewNoun('the the bob', '', 'bob', self.definite_uncountable))

    def test_plural_returns_plural_noun(self):
        answer = NewNoun('bob').plural()
        self.assertEqual(answer, NewNoun('bobs', '', 'bob', self.plural))

        answer = NewNoun('a bob', '', 'bob', self.indefinite).plural()
        self.assertEqual(answer, NewNoun('a bobs', '', 'bob', self.plural))

        answer = NewNoun('the bob', '', 'bob', self.definite).plural()
        self.assertEqual(answer, NewNoun('the bobs', '', 'bob', self.definite_plural))

        # answer = NewNoun('bobs', '', 'bob', self.plural).plural()
        # self.assertEqual(answer, NewNoun('bobses', '', 'bob', self.plural))

        answer = NewNoun('the bobs', '', 'bob', self.definite_plural).plural()  # TODO yes or no?
        self.assertEqual(answer, NewNoun('the bobs', '', 'bob', self.definite_plural))

    def test_plural_with_f_and_fe_ending_nouns(self):
        self.assertEqual(NewNoun('life').plural(), NewNoun('lives', '', 'life', self.plural))
        self.assertEqual(NewNoun('waif').plural(), NewNoun('waifs', '', 'waif', self.plural))
        self.assertEqual(NewNoun('calf').plural(), NewNoun('calves', '', 'calf', self.plural))
        self.assertEqual(NewNoun('leaf').plural(), NewNoun('leaves', '', 'leaf', self.plural))

    def test_capitalize_all(self):
        original = NewNoun('bob')
        basic = original.capitalize()
        self.assertEqual(basic, NewNoun('Bob', '', 'bob'))

        uncountable = NewNoun.uncountable_noun('bob').capitalize()
        self.assertEqual(uncountable, NewNoun('Bob', '', 'bob', Tags([wt.UNCOUNTABLE])))

        definite_uncountable = NewNoun.uncountable_noun('bob').definite().capitalize()
        self.assertEqual(definite_uncountable, NewNoun('The bob', '', 'bob', self.definite_uncountable))

        indefinite = original.indefinite().capitalize()
        self.assertEqual(indefinite, NewNoun('A bob', '', 'bob', self.indefinite))

        definite = original.definite().capitalize()
        self.assertEqual(definite, NewNoun('The bob', '', 'bob', self.definite))

        plural = original.plural().capitalize()
        self.assertEqual(plural, NewNoun('Bobs', '', 'bob', self.plural))

        definite_plural = original.definite().plural().capitalize()
        self.assertEqual(definite_plural, NewNoun('The bobs', '', 'bob', self.definite_plural))

        plural_definite = original.plural().definite().capitalize()
        self.assertEqual(plural_definite, NewNoun('The bobs', '', 'bob', self.definite_plural))

        wacky = original.plural().capitalize().definite()
        self.assertEqual(wacky, NewNoun('the Bobs', '', 'bob', self.definite_plural))

        proper = NewNoun.proper_noun('Bob')
        self.assertEqual(proper.capitalize(), proper)

        proper_plural = NewNoun.proper_noun('The Bobs', plural=True)
        self.assertEqual(proper_plural.capitalize(), proper_plural)

    def test_de_capitalize_all(self):
        original = NewNoun('bob')
        basic = original.capitalize()
        self.assertEqual(basic.de_capitalize(), NewNoun('bob', '', 'bob'))

        uncountable = NewNoun.uncountable_noun('bob').capitalize()
        self.assertEqual(uncountable.de_capitalize(), NewNoun.uncountable_noun('bob'))

        definite_uncountable = NewNoun.uncountable_noun('bob').definite().capitalize()
        self.assertEqual(definite_uncountable.de_capitalize(), NewNoun('the bob', '', 'bob', self.definite_uncountable))

        indefinite = original.indefinite().capitalize()
        self.assertEqual(indefinite.de_capitalize(), NewNoun('a bob', '', 'bob', self.indefinite))

        definite = original.definite().capitalize()
        self.assertEqual(definite.de_capitalize(), NewNoun('the bob', '', 'bob', self.definite))

        plural = original.plural().capitalize()
        self.assertEqual(plural.de_capitalize(), NewNoun('bobs', '', 'bob', self.plural))

        definite_plural = original.definite().plural().capitalize()
        self.assertEqual(definite_plural.de_capitalize(), NewNoun('the bobs', '', 'bob', self.definite_plural))

        plural_definite = original.plural().definite().capitalize()
        self.assertEqual(plural_definite.de_capitalize(), NewNoun('the bobs', '', 'bob', self.definite_plural))

        wacky = original.plural().capitalize().definite()
        self.assertEqual(wacky.de_capitalize(), NewNoun('the Bobs', '', 'bob', self.definite_plural))

        proper = NewNoun.proper_noun('Bob').de_capitalize()
        self.assertEqual(NewNoun('Bob', '', 'Bob', self.proper), proper)

        proper_plural = NewNoun.proper_noun('The Bobs', plural=True).de_capitalize()
        self.assertEqual(NewNoun('The Bobs', '', 'The Bobs', self.plural_proper), proper_plural)

    def test_repr(self):
        self.assertEqual(repr(NewNoun('bob')), "NewNoun('bob', '', 'bob', Tags([]))")
        self.assertEqual(repr(NewNoun.uncountable_noun('bob')),
                         "NewNoun('bob', '', 'bob', Tags([WordTag.UNCOUNTABLE]))")
        self.assertEqual(repr(NewNoun.proper_noun('Bob', plural=True)),
                         "NewNoun('Bob', '', 'Bob', Tags([WordTag.PLURAL, WordTag.PROPER]))")

    def test_to_base_noun_keeps_plural_info(self):
        self.assertEqual(NewNoun('bob', 'boba').to_base_noun(), NewNoun('bob', 'boba'))

    def test_to_base_noun_no_special_plural(self):
        original = NewNoun('bob')
        self.assertEqual(original.plural().to_base_noun(), original)
        self.assertEqual(original.indefinite().to_base_noun(), original)
        self.assertEqual(original.definite().to_base_noun(), original)
        self.assertEqual(original.definite().plural().to_base_noun(), original)
        self.assertEqual(original.capitalize().plural().definite().to_base_noun(), original)

    def test_to_base_noun_special_plural(self):
        original = NewNoun('bob', 'boberino')
        expected = NewNoun('bob', 'boberino')
        self.assertEqual(original.plural().to_base_noun(), expected)
        self.assertEqual(original.indefinite().to_base_noun(), expected)
        self.assertEqual(original.definite().to_base_noun(), expected)
        self.assertEqual(original.definite().plural().to_base_noun(), expected)
        self.assertEqual(original.capitalize().plural().definite().to_base_noun(), expected)

    def test_hash(self):
        self.assertEqual(hash(NewNoun('bob')),
                         hash("hash of NewNoun('bob', '', 'bob', Tags([]))"))
        self.assertEqual(hash(NewNoun('bob').definite()),
                         hash("hash of NewNoun('the bob', '', 'bob', Tags([WordTag.DEFINITE]))"))

    def test_definite_plural(self):
        noun = NewNoun('dog')
        new = noun.definite().plural()
        self.assertEqual(new, NewNoun('the dogs', '', 'dog', self.definite_plural))

        irregular = NewNoun('child', 'children')
        new = irregular.definite().plural()
        self.assertEqual(new, NewNoun('the children', 'children', 'child', self.definite_plural))

    def test_plural_definite(self):
        noun = NewNoun('dog')
        new = noun.plural().definite()
        self.assertEqual(new, NewNoun('the dogs', '', 'dog', self.definite_plural))

        irregular = NewNoun('child', 'children')
        new = irregular.plural().definite()
        self.assertEqual(new, NewNoun('the children', 'children', 'child', self.definite_plural))

    def test_indefinite_plural(self):
        noun = NewNoun('dog')
        new = noun.indefinite().plural()
        self.assertEqual(new, NewNoun('a dogs', '', 'dog', self.plural))

        irregular = NewNoun('child', 'children')
        new = irregular.indefinite().plural()
        self.assertEqual(new, NewNoun('a children', 'children', 'child', self.plural))

    def test_plural_indefinite(self):
        noun = NewNoun('dog')
        new = noun.plural().indefinite()
        self.assertEqual(new, NewNoun('a dogs', '', 'dog', self.indefinite))

        irregular = NewNoun('child', 'children')
        new = irregular.plural().indefinite()
        self.assertEqual(new, NewNoun('a children', 'children', 'child', self.indefinite))

    def test_uncountable_plural(self):
        noun = NewNoun.uncountable_noun('water')
        self.assertEqual(noun.plural(), NewNoun('waters', '', 'water', Tags([wt.UNCOUNTABLE, wt.PLURAL])))

    def test_definite_uncountable_plural(self):
        noun = NewNoun.uncountable_noun('water')
        self.assertEqual(noun.definite().plural(), NewNoun('the waters', '', 'water',
                                                           self.definite_plural.add(wt.UNCOUNTABLE)))

    def test_proper_noun_plural(self):
        noun = NewNoun.proper_noun('Bob')
        self.assertEqual(noun.plural(), NewNoun('Bobs', '', 'Bob', self.plural_proper))

    def test_plural_proper_noun_plural(self):
        noun = NewNoun('Bobs', '', 'Bob', self.plural_proper)
        self.assertEqual(noun.plural(), noun)

    def test_proper_noun_definite(self):
        noun = NewNoun.proper_noun('Bob').definite()
        self.assertEqual(noun, NewNoun('the Bob', '', 'Bob', self.definite))

        noun = NewNoun.proper_noun('Bobs', True).definite()
        self.assertEqual(noun, NewNoun('the Bobs', '', 'Bobs', self.definite_plural))

    def test_proper_noun_definite_and_plural(self):
        noun = NewNoun.proper_noun('Bob').plural().definite()
        self.assertEqual(noun, NewNoun('the Bobs', '', 'Bob', self.definite_plural))

        noun = NewNoun.proper_noun('Bob').definite().plural()
        self.assertEqual(noun, NewNoun('the Bobs', '', 'Bob', self.definite_plural))

    def test_proper_noun_indefinite_an(self):
        noun = NewNoun.proper_noun('Ed')
        plural = noun.plural()

        self.assertEqual(noun.indefinite(), NewNoun('an Ed', '', 'Ed', self.indefinite))
        self.assertEqual(plural.indefinite(), NewNoun('an Eds', '', 'Ed', self.indefinite))

    def test_proper_noun_capitalize(self):
        noun = NewNoun.proper_noun('Ed')
        plural = noun.plural()

        self.assertEqual(noun.capitalize(), noun)
        self.assertEqual(plural.capitalize(), plural)

        sports_team = NewNoun.proper_noun('the Guys', plural=True)
        self.assertEqual(sports_team.capitalize(), NewNoun('The Guys', '', 'the Guys', self.plural_proper))

    def test_proper_noun_de_capitalize_starts_with_capital(self):
        noun = NewNoun.proper_noun('Joe')
        plural = noun.plural()

        self.assertEqual(noun.de_capitalize(), noun)
        self.assertEqual(plural.de_capitalize(), plural)

    def test_proper_noun_de_capitalize_starts_with_lower_case(self):
        noun = NewNoun.proper_noun('the Dude')
        plural = noun.plural()
        capital_noun = noun.capitalize()
        capital_plural = plural.capitalize()

        self.assertEqual(noun.de_capitalize(), noun)
        self.assertEqual(capital_noun.de_capitalize(), noun)
        self.assertEqual(plural.de_capitalize(), plural)
        self.assertEqual(capital_plural.de_capitalize(), plural)

    def test_de_capitalize_special_cases(self):
        for value in ('BMW', 'dog', 'Practice Book'):
            noun = NewNoun(value)
            plural = noun.plural()
            definite = noun.definite()
            indefinite = noun.indefinite()

            for test_noun in [noun, plural, definite, indefinite]:
                self.assertEqual(test_noun, test_noun.capitalize().de_capitalize())

