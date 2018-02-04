import string
import unittest

from sentences.words.new_word import NewNoun, get_plural_value, get_article
from sentences.words.word import Word
from sentences.words.wordtools.wordtag import WordTag
from sentences.words.wordtools.tags import Tags


class TestNoun(unittest.TestCase):

    def setUp(self):
        self.indefinite = Tags([WordTag.INDEFINITE])
        self.definite = Tags([WordTag.DEFINITE])
        self.plural = Tags([WordTag.PLURAL])
        self.definite_plural = Tags([WordTag.DEFINITE, WordTag.PLURAL])
        self.definite_uncountable = Tags([WordTag.DEFINITE, WordTag.UNCOUNTABLE])
        self.proper = Tags([WordTag.PROPER])
        self.plural_proper = Tags([WordTag.PLURAL, WordTag.PROPER])

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

    def test_get_article_no_article(self):
        self.assertEqual(get_article('sjdkf'), '')
        self.assertEqual(get_article('sdf sjdkf'), '')
        self.assertEqual(get_article(' sjdkf'), '')

    def test_get_article_all_articles(self):
        self.assertEqual(get_article('a dog'), 'a ')
        self.assertEqual(get_article('A dog'), 'A ')
        self.assertEqual(get_article('an egg'), 'an ')
        self.assertEqual(get_article('An egg'), 'An ')
        self.assertEqual(get_article('the dog'), 'the ')
        self.assertEqual(get_article('The dog'), 'The ')

    def test_noun_values(self):
        test = NewNoun('a', 'b', 'c', Tags([WordTag.DEFINITE]))
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, 'b')
        self.assertEqual(test.base_noun, 'c')
        self.assertEqual(test.tags, Tags([WordTag.DEFINITE]))

    def test_noun_empty_values(self):
        test = NewNoun('a')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, '')
        self.assertEqual(test.base_noun, 'a')
        self.assertEqual(test.tags, Tags([]))

    def test_equality_true_false_by_value(self):
        test = NewNoun('a', 'b', 'c', tags=self.proper)
        equal = NewNoun('a', 'b', 'c', tags=self.proper)
        not_equal = NewNoun('x', 'b', 'c', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_irregular_plural(self):
        test = NewNoun('a', 'b', 'c', tags=self.proper)
        equal = NewNoun('a', 'b', 'c', tags=self.proper)
        not_equal = NewNoun('a', 'x', 'c', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_base_noun(self):
        test = NewNoun('a', 'b', 'c', tags=self.proper)
        equal = NewNoun('a', 'b', 'c', tags=self.proper)
        not_equal = NewNoun('a', 'b', 'x', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_tags(self):
        test = NewNoun('a', 'b', 'c', tags=self.proper)
        equal = NewNoun('a', 'b', 'c', tags=self.proper)
        not_equal = NewNoun('a', 'b', 'c', tags=self.plural_proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_eq_must_be_noun(self):
        self.assertNotEqual(NewNoun('bob'), Word('bob'))

    def test_uncountable_noun_class_method(self):
        test = NewNoun.uncountable_noun('water')
        self.assertEqual(test, NewNoun('water', '', 'water', Tags([WordTag.UNCOUNTABLE])))

    def test_proper_noun_singular_class_method(self):
        test_1 = NewNoun.proper_noun('Joe')
        test_2 = NewNoun.proper_noun('Joe', plural=False)

        expected = NewNoun('Joe', '', 'Joe', Tags([WordTag.PROPER]))
        self.assertEqual(test_1, expected)
        self.assertEqual(test_2, expected)

    def test_proper_noun_plural_class_method(self):
        test = NewNoun.proper_noun('the Joneses', plural=True)
        self.assertEqual(test, NewNoun('the Joneses', '', 'the Joneses', Tags([WordTag.PROPER, WordTag.PLURAL])))

    def test_repr(self):
        self.assertEqual(repr(NewNoun('bob')), "NewNoun('bob', '', 'bob', Tags([]))")
        self.assertEqual(repr(NewNoun.uncountable_noun('bob')),
                         "NewNoun('bob', '', 'bob', Tags([WordTag.UNCOUNTABLE]))")
        self.assertEqual(repr(NewNoun.proper_noun('Bob', plural=True)),
                         "NewNoun('Bob', '', 'Bob', Tags([WordTag.PLURAL, WordTag.PROPER]))")

    def test_hash(self):
        self.assertEqual(hash(NewNoun('bob')),
                         hash("hash of NewNoun('bob', '', 'bob', Tags([]))"))
        self.assertEqual(hash(NewNoun('bob').definite()),
                         hash("hash of NewNoun('the bob', '', 'bob', Tags([WordTag.DEFINITE]))"))

    def test_capitalize_simple_case(self):
        noun = NewNoun('dog').capitalize()
        self.assertIsInstance(noun, NewNoun)
        self.assertEqual(noun, NewNoun('Dog', '', 'dog'))

    def test_capitalize_capital_letters_in_value(self):
        noun = NewNoun('the DUDE').capitalize()
        self.assertEqual(noun, NewNoun('The DUDE', '', 'the DUDE'))

    def test_capitalize_first_letter_capital(self):
        noun = NewNoun('ABC')
        self.assertEqual(noun, noun.capitalize())

    def test_capitalize_preserves_tags(self):
        noun = NewNoun('ABC', tags=self.plural_proper)
        self.assertEqual(noun, noun.capitalize())

    def test_de_capitalize_simple_case(self):
        noun = NewNoun('Dog', '', 'dog').de_capitalize()
        self.assertIsInstance(noun, NewNoun)
        self.assertEqual(noun, NewNoun('dog', '', 'dog'))

    def test_de_capitalize_capital_letters_in_value(self):
        noun = NewNoun('The DUDE', '', 'the DUDE').de_capitalize()
        self.assertEqual(noun, NewNoun('the DUDE', '', 'the DUDE'))

    def test_de_capitalize_first_letter_not_capital(self):
        noun = NewNoun('abc')
        self.assertEqual(noun, noun.de_capitalize())

    def test_de_capitalize_preserves_tags(self):
        noun = NewNoun('abc', tags=self.plural_proper)
        self.assertEqual(noun, noun.de_capitalize())

    def test_de_capitalize_base_capital_and_value_starts_with_base(self):
        noun = NewNoun('ABCs', '', 'ABC')
        self.assertEqual(noun.de_capitalize(), noun)

    def test_de_capitalize_base_capital_and_value_does_not_start_with_base(self):
        noun = NewNoun('The ABCs', '', 'ABC')
        self.assertEqual(noun.de_capitalize(), NewNoun('the ABCs', '', 'ABC'))

    def test_de_capitalize_base_lower_case_and_value_starts_with_base(self):
        noun = NewNoun('cats', '', 'cat')
        self.assertEqual(noun.de_capitalize(), noun)

    def test_de_capitalize_base_lower_case_and_value_does_not_start_with_base(self):
        noun = NewNoun('The cats', '', 'cat')
        self.assertEqual(noun.de_capitalize(), NewNoun('the cats', '', 'cat'))

    def test_capitalize_de_capitalize_regression_test(self):
        for value in ('BMW', 'dog', 'Practice Book'):
            noun = NewNoun(value)
            plural = noun.plural()
            definite = noun.definite()
            indefinite = noun.indefinite()

            for test_noun in [noun, plural, definite, indefinite]:
                self.assertEqual(test_noun, test_noun.capitalize().de_capitalize())

    def test_bold(self):
        noun = NewNoun('thing', tags=self.plural_proper)
        expected = NewNoun('<bold>thing</bold>', '', 'thing', tags=self.plural_proper)

        self.assertEqual(noun.bold(), expected)
        self.assertEqual(noun.bold().bold().bold(), expected)

    def test_definite(self):
        self.assertEqual(NewNoun('hour').definite(), NewNoun('the hour', '', 'hour', tags=self.definite))
        self.assertEqual(NewNoun('happy hour').definite(),
                         NewNoun('the happy hour',  '', 'happy hour', tags=self.definite))

    def test_definite_preserves_plural(self):
        self.assertEqual(NewNoun('octopus', 'octopodes').definite(),
                         NewNoun('the octopus', 'octopodes', 'octopus', tags=self.definite))

    def test_definite_adds_definite_tag(self):
        tags = Tags([WordTag.PLURAL, WordTag.PAST])
        expected_tags = Tags([WordTag.PLURAL, WordTag.PAST, WordTag.DEFINITE])

        noun = NewNoun('x', tags=tags)
        self.assertEqual(noun.definite(), NewNoun('the x', '', 'x', tags=expected_tags))

    def test_definite_does_not_alter_definite_noun(self):
        noun = NewNoun('x').definite()
        self.assertEqual(noun.definite(), noun)
        self.assertEqual(noun.definite().definite().definite(), noun)

    def test_definite_removes_proper_tag(self):
        expected_tags = Tags([WordTag.PLURAL, WordTag.DEFINITE])
        noun = NewNoun.proper_noun('Xs', plural=True)

        self.assertEqual(noun.definite(), NewNoun('the Xs', '', 'Xs', tags=expected_tags))
        self.assertTrue(noun.has_tags(WordTag.PROPER))

    def test_definite_removes_indefinite_tag(self):
        expected_tags = Tags([WordTag.DEFINITE])
        noun = NewNoun('x').indefinite()

        self.assertEqual(noun.definite(), NewNoun('the a x', '', 'x', tags=expected_tags))
        self.assertTrue(noun.has_tags(WordTag.INDEFINITE))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(NewNoun('hour').indefinite(), NewNoun('a hour', '', 'hour', tags=self.indefinite))
        self.assertEqual(NewNoun('happy hour').indefinite(),
                         NewNoun('a happy hour', '', 'happy hour', tags=self.indefinite))

    def test_indefinite_vowel_start(self):
        self.assertEqual(NewNoun('elephant').indefinite(), NewNoun('an elephant', '', 'elephant', tags=self.indefinite))
        self.assertEqual(NewNoun('old man').indefinite(), NewNoun('an old man', '', 'old man', tags=self.indefinite))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(NewNoun(vowel).indefinite(), NewNoun('an ' + vowel, '', vowel, tags=self.indefinite))

    def test_indefinite_all_non_vowels(self):
        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(NewNoun(consonant).indefinite(), NewNoun('a ' + consonant, '', consonant,
                                                                          self.indefinite))

    def test_indefinite_only_has_indefinite_tag(self):
        uncountable = NewNoun.uncountable_noun('water')
        self.assertEqual(uncountable.tags, Tags([WordTag.UNCOUNTABLE]))
        proper = NewNoun.proper_noun('Joes', plural=True)
        self.assertEqual(proper.tags, self.plural_proper)

        self.assertEqual(uncountable.indefinite(), NewNoun('a water', '', 'water', tags=self.indefinite))
        self.assertEqual(proper.indefinite(), NewNoun('a Joes', '', 'Joes', tags=self.indefinite))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(NewNoun('octopus', 'octopodes').indefinite(),
                         NewNoun('an octopus', 'octopodes', 'octopus', self.indefinite))

    def test_indefinite_does_not_change_indefinite_noun(self):
        noun = NewNoun('a').indefinite()
        self.assertEqual(noun.indefinite(), noun)
        self.assertEqual(noun.indefinite().indefinite().indefinite(), noun)

    def test_plural_no_irregular_plural(self):
        self.assertEqual(NewNoun('bob').plural(), NewNoun('bobs', '', 'bob', self.plural))
        self.assertEqual(NewNoun('bobo').plural(), NewNoun('boboes', '', 'bobo', self.plural))
        self.assertEqual(NewNoun('half').plural(), NewNoun('halves', '', 'half', self.plural))
        self.assertEqual(NewNoun('goof').plural(), NewNoun('goofs', '', 'goof', self.plural))
        self.assertEqual(NewNoun('baby').plural(), NewNoun('babies', '', 'baby', self.plural))
        self.assertEqual(NewNoun('ex').plural(), NewNoun('exes', '', 'ex', self.plural))

    def test_plural_with_special_f_and_fe_ending_nouns(self):
        self.assertEqual(NewNoun('life').plural(), NewNoun('lives', '', 'life', self.plural))
        self.assertEqual(NewNoun('waif').plural(), NewNoun('waifs', '', 'waif', self.plural))
        self.assertEqual(NewNoun('calf').plural(), NewNoun('calves', '', 'calf', self.plural))
        self.assertEqual(NewNoun('leaf').plural(), NewNoun('leaves', '', 'leaf', self.plural))

    def test_plural_with_irregular_plural(self):
        self.assertEqual(NewNoun('bobo', 'bobi').plural(), NewNoun('bobi', 'bobi', 'bobo', self.plural))

    def test_plural_with_articles_no_irregular_plural(self):
        self.assertEqual(NewNoun('a life').plural(), NewNoun('a lives', '', 'a life', self.plural))

    def test_plural_with_articles_irregular_plural(self):
        self.assertEqual(NewNoun('A bobo', 'bobi', 'bobo').plural(), NewNoun('A bobi', 'bobi', 'bobo', self.plural))
        self.assertEqual(NewNoun('the bobo', 'bobi', 'bobo').plural(), NewNoun('the bobi', 'bobi', 'bobo', self.plural))




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
        self.assertEqual(noun.plural(), NewNoun('waters', '', 'water', Tags([WordTag.PLURAL])))

    def test_definite_uncountable_plural(self):
        noun = NewNoun.uncountable_noun('water')
        self.assertEqual(noun.definite().plural(), NewNoun('the waters', '', 'water', tags=self.definite_plural))

    def test_proper_noun_plural(self):
        noun = NewNoun.proper_noun('Bob')
        self.assertEqual(noun.plural(), NewNoun('Bobs', '', 'Bob', self.plural_proper))

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



