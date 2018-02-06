import string
import unittest

from sentences.words.noun import Noun, get_plural_value, get_article
from sentences.words.basicword import BasicWord
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

    def test_get_article_two_articles(self):
        self.assertEqual(get_article('a the dog'), 'a ')

    def test_get_article_no_space(self):
        self.assertEqual(get_article('thedog'), '')

    def test_get_article_article_in_middle(self):
        self.assertEqual(get_article('dog the dog'), '')

    def test_noun_values(self):
        test = Noun('a', 'b', 'c', Tags([WordTag.DEFINITE]))
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, 'b')
        self.assertEqual(test.base_noun, 'c')
        self.assertEqual(test.tags, Tags([WordTag.DEFINITE]))

    def test_noun_empty_values(self):
        test = Noun('a')
        self.assertEqual(test.value, 'a')
        self.assertEqual(test.irregular_plural, '')
        self.assertEqual(test.base_noun, 'a')
        self.assertEqual(test.tags, Tags([]))

    def test_equality_true_false_by_value(self):
        test = Noun('a', 'b', 'c', tags=self.proper)
        equal = Noun('a', 'b', 'c', tags=self.proper)
        not_equal = Noun('x', 'b', 'c', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_irregular_plural(self):
        test = Noun('a', 'b', 'c', tags=self.proper)
        equal = Noun('a', 'b', 'c', tags=self.proper)
        not_equal = Noun('a', 'x', 'c', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_base_noun(self):
        test = Noun('a', 'b', 'c', tags=self.proper)
        equal = Noun('a', 'b', 'c', tags=self.proper)
        not_equal = Noun('a', 'b', 'x', tags=self.proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_equality_true_false_by_tags(self):
        test = Noun('a', 'b', 'c', tags=self.proper)
        equal = Noun('a', 'b', 'c', tags=self.proper)
        not_equal = Noun('a', 'b', 'c', tags=self.plural_proper)

        self.assertEqual(test, equal)
        self.assertNotEqual(test, not_equal)

    def test_eq_must_be_noun(self):
        self.assertNotEqual(Noun('bob'), BasicWord('bob'))

    def test_uncountable_noun_class_method(self):
        test = Noun.uncountable_noun('water')
        self.assertEqual(test, Noun('water', '', 'water', Tags([WordTag.UNCOUNTABLE])))

    def test_proper_noun_singular_class_method(self):
        test_1 = Noun.proper_noun('Joe')
        test_2 = Noun.proper_noun('Joe', plural=False)

        expected = Noun('Joe', '', 'Joe', Tags([WordTag.PROPER]))
        self.assertEqual(test_1, expected)
        self.assertEqual(test_2, expected)

    def test_proper_noun_plural_class_method(self):
        test = Noun.proper_noun('the Joneses', plural=True)
        self.assertEqual(test, Noun('the Joneses', '', 'the Joneses', Tags([WordTag.PROPER, WordTag.PLURAL])))

    def test_repr(self):
        self.assertEqual(repr(Noun('bob')), "Noun('bob', '', 'bob', Tags([]))")
        self.assertEqual(repr(Noun.uncountable_noun('bob')),
                         "Noun('bob', '', 'bob', Tags([WordTag.UNCOUNTABLE]))")
        self.assertEqual(repr(Noun.proper_noun('Bob', plural=True)),
                         "Noun('Bob', '', 'Bob', Tags([WordTag.PLURAL, WordTag.PROPER]))")
        self.assertEqual(repr(Noun('a', 'b', 'c', Tags([WordTag.PLURAL]))),
                         "Noun('a', 'b', 'c', Tags([WordTag.PLURAL]))")

    def test_hash(self):
        self.assertEqual(hash(Noun('bob')),
                         hash("hash of Noun('bob', '', 'bob', Tags([]))"))
        self.assertEqual(hash(Noun('bob').definite()),
                         hash("hash of Noun('the bob', '', 'bob', Tags([WordTag.DEFINITE]))"))

    def test_capitalize_simple_case(self):
        noun = Noun('dog').capitalize()
        self.assertEqual(noun, Noun('Dog', '', 'dog'))

    def test_capitalize_capital_letters_in_value(self):
        noun = Noun('the DUDE').capitalize()
        self.assertEqual(noun, Noun('The DUDE', '', 'the DUDE'))

    def test_capitalize_first_letter_capital(self):
        noun = Noun('ABC')
        self.assertEqual(noun, noun.capitalize())

    def test_capitalize_preserves_tags(self):
        noun = Noun('ABC', tags=self.plural_proper)
        self.assertEqual(noun, noun.capitalize())

    def test_de_capitalize_simple_case(self):
        noun = Noun('Dog', '', 'dog').de_capitalize()
        self.assertIsInstance(noun, Noun)
        self.assertEqual(noun, Noun('dog', '', 'dog'))

    def test_de_capitalize_capital_letters_in_value(self):
        noun = Noun('The DUDE', '', 'the DUDE').de_capitalize()
        self.assertEqual(noun, Noun('the DUDE', '', 'the DUDE'))

    def test_de_capitalize_first_letter_not_capital(self):
        noun = Noun('abc')
        self.assertEqual(noun, noun.de_capitalize())

    def test_de_capitalize_preserves_tags(self):
        noun = Noun('abc', tags=self.plural_proper)
        self.assertEqual(noun, noun.de_capitalize())

    def test_de_capitalize_base_capital_and_value_starts_with_base(self):
        noun = Noun('ABCs', '', 'ABC')
        self.assertEqual(noun.de_capitalize(), noun)

    def test_de_capitalize_base_capital_and_value_does_not_start_with_base(self):
        noun = Noun('The ABCs', '', 'ABC')
        self.assertEqual(noun.de_capitalize(), Noun('the ABCs', '', 'ABC'))

    def test_de_capitalize_base_lower_case_and_value_starts_with_base(self):
        noun = Noun('cats', '', 'cat')
        self.assertEqual(noun.de_capitalize(), noun)

    def test_de_capitalize_base_lower_case_and_value_does_not_start_with_base(self):
        noun = Noun('The cats', '', 'cat')
        self.assertEqual(noun.de_capitalize(), Noun('the cats', '', 'cat'))

    def test_capitalize_de_capitalize_regression_test(self):
        for value in ('BMW', 'dog', 'Practice Book'):
            noun = Noun(value)
            plural = noun.plural()
            definite = noun.definite()
            indefinite = noun.indefinite()

            for test_noun in [noun, plural, definite, indefinite]:
                self.assertEqual(test_noun, test_noun.capitalize().de_capitalize())

    def test_bold(self):
        noun = Noun('thing', tags=self.plural_proper)
        expected = Noun('<bold>thing</bold>', '', 'thing', tags=self.plural_proper)

        self.assertEqual(noun.bold(), expected)
        self.assertEqual(noun.bold().bold().bold(), expected)

    def test_definite(self):
        self.assertEqual(Noun('hour').definite(), Noun('the hour', '', 'hour', tags=self.definite))
        self.assertEqual(Noun('ABCs', '', 'ABC').definite(),
                         Noun('the ABCs', '', 'ABC', tags=self.definite))

    def test_definite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').definite(),
                         Noun('the octopus', 'octopodes', 'octopus', tags=self.definite))

    def test_definite_adds_definite_tag(self):
        tags = Tags([WordTag.PLURAL, WordTag.PAST])
        expected_tags = Tags([WordTag.PLURAL, WordTag.PAST, WordTag.DEFINITE])

        noun = Noun('x', tags=tags)
        self.assertEqual(noun.definite(), Noun('the x', '', 'x', tags=expected_tags))

    def test_definite_does_not_alter_definite_noun(self):
        noun = Noun('x').definite()
        self.assertEqual(noun.definite(), noun)
        self.assertEqual(noun.definite().definite().definite(), noun)

    def test_definite_removes_proper_tag(self):
        noun = Noun.proper_noun('Xs', plural=True)
        self.assertEqual(noun.tags, self.plural_proper)

        self.assertEqual(noun.definite(), Noun('the Xs', '', 'Xs', tags=self.definite_plural))

    def test_definite_removes_indefinite_tag(self):
        noun = Noun('x').indefinite()
        self.assertEqual(noun.tags, self.indefinite)

        self.assertEqual(noun.definite(), Noun('the a x', '', 'x', tags=self.definite))

    def test_indefinite_no_vowel_start(self):
        self.assertEqual(Noun('hour').indefinite(), Noun('a hour', '', 'hour', tags=self.indefinite))
        self.assertEqual(Noun('happy hour').indefinite(),
                         Noun('a happy hour', '', 'happy hour', tags=self.indefinite))

    def test_indefinite_vowel_start(self):
        self.assertEqual(Noun('elephant').indefinite(), Noun('an elephant', '', 'elephant', tags=self.indefinite))
        self.assertEqual(Noun('old man').indefinite(), Noun('an old man', '', 'old man', tags=self.indefinite))

    def test_indefinite_all_vowels(self):
        for vowel in 'aeiouAEIOU':
            self.assertEqual(Noun(vowel).indefinite(), Noun('an ' + vowel, '', vowel, tags=self.indefinite))

    def test_indefinite_all_non_vowels(self):
        vowels = 'aeiouAEIOU'
        for consonant in string.ascii_letters:
            if consonant not in vowels:
                self.assertEqual(Noun(consonant).indefinite(), Noun('a ' + consonant, '', consonant,
                                                                    tags=self.indefinite))

    def test_indefinite_only_has_indefinite_tag(self):
        uncountable = Noun.uncountable_noun('water')
        self.assertEqual(uncountable.tags, Tags([WordTag.UNCOUNTABLE]))
        proper = Noun.proper_noun('Joes', plural=True)
        self.assertEqual(proper.tags, self.plural_proper)

        self.assertEqual(uncountable.indefinite(), Noun('a water', '', 'water', tags=self.indefinite))
        self.assertEqual(proper.indefinite(), Noun('a Joes', '', 'Joes', tags=self.indefinite))

    def test_indefinite_preserves_plural(self):
        self.assertEqual(Noun('octopus', 'octopodes').indefinite(),
                         Noun('an octopus', 'octopodes', 'octopus', tags=self.indefinite))

    def test_indefinite_does_not_change_indefinite_noun(self):
        noun = Noun('a').indefinite()
        self.assertEqual(noun.indefinite(), noun)
        self.assertEqual(noun.indefinite().indefinite().indefinite(), noun)

    def test_plural_no_irregular_plural(self):
        self.assertEqual(Noun('bob').plural(), Noun('bobs', '', 'bob', tags=self.plural))
        self.assertEqual(Noun('bobo').plural(), Noun('boboes', '', 'bobo', tags=self.plural))
        self.assertEqual(Noun('half').plural(), Noun('halves', '', 'half', tags=self.plural))
        self.assertEqual(Noun('goof').plural(), Noun('goofs', '', 'goof', tags=self.plural))
        self.assertEqual(Noun('baby').plural(), Noun('babies', '', 'baby', tags=self.plural))
        self.assertEqual(Noun('ex').plural(), Noun('exes', '', 'ex', tags=self.plural))

    def test_plural_with_special_f_and_fe_ending_nouns(self):
        self.assertEqual(Noun('life').plural(), Noun('lives', '', 'life', tags=self.plural))
        self.assertEqual(Noun('waif').plural(), Noun('waifs', '', 'waif', tags=self.plural))
        self.assertEqual(Noun('calf').plural(), Noun('calves', '', 'calf', tags=self.plural))
        self.assertEqual(Noun('leaf').plural(), Noun('leaves', '', 'leaf', tags=self.plural))

    def test_plural_with_irregular_plural(self):
        self.assertEqual(Noun('bobo', 'bobi').plural(), Noun('bobi', 'bobi', 'bobo', tags=self.plural))

    def test_plural_with_articles_no_irregular_plural(self):
        articles = ('a ', 'A ', 'an ', 'An ', 'the ', 'The ')
        for article in articles:
            base_value = article + 'thing'
            self.assertEqual(Noun(base_value).plural(),
                             Noun(base_value + 's', '', base_value, tags=self.plural))

    def test_plural_with_articles_irregular_plural(self):
        articles = ('a ', 'A ', 'an ', 'An ', 'the ', 'The ')
        for article in articles:
            base_value = article + 'child'
            plural_value = article + 'children'
            self.assertEqual(Noun(base_value, 'children').plural(),
                             Noun(plural_value, 'children', base_value, tags=self.plural))

    def test_plural_adds_plural_tag(self):
        noun = Noun('dog', tags=Tags())
        definite = Noun('the dog', '', 'dog', tags=self.definite)
        proper = Noun('Joe', tags=self.proper)

        self.assertEqual(noun.plural(), Noun('dogs', '', 'dog', tags=self.plural))
        self.assertEqual(definite.plural(), Noun('the dogs', '', 'dog', tags=self.definite_plural))
        self.assertEqual(proper.plural(), Noun('Joes', '', 'Joe', tags=self.plural_proper))

    def test_plural_removes_indefinite_tag(self):
        noun = Noun('a dog', '', 'dog', tags=self.indefinite)
        self.assertEqual(noun.plural(), Noun('a dogs', '', 'dog', tags=self.plural))

    def test_plural_removes_uncountable_tag(self):
        noun = Noun('water', tags=Tags([WordTag.UNCOUNTABLE]))
        self.assertEqual(noun.plural(), Noun('waters', '', 'water', tags=self.plural))

        definite = Noun('the water', '',  'water', tags=self.definite_uncountable)
        self.assertEqual(definite.plural(), Noun('the waters', '', 'water', tags=self.definite_plural))

    def test_plural_does_not_change_a_plural_noun(self):
        plural = Noun('dog').plural()
        definite_plural = Noun('dog').definite().plural()
        proper_plural = Noun.proper_noun('the Joneses', plural=True)

        self.assertEqual(plural.plural(), plural)
        self.assertEqual(plural.plural().plural().plural(), plural)

        self.assertEqual(definite_plural.plural(), definite_plural)
        self.assertEqual(definite_plural.plural().plural().plural(), definite_plural)

        self.assertEqual(proper_plural.plural(), proper_plural)
        self.assertEqual(proper_plural.plural().plural().plural(), proper_plural)

    def test_definite_plural(self):
        noun = Noun('dog')
        new = noun.definite().plural()
        self.assertEqual(new, Noun('the dogs', '', 'dog', self.definite_plural))

        irregular = Noun('child', 'children')
        new = irregular.definite().plural()
        self.assertEqual(new, Noun('the children', 'children', 'child', self.definite_plural))

    def test_plural_definite(self):
        noun = Noun('dog')
        new = noun.plural().definite()
        self.assertEqual(new, Noun('the dogs', '', 'dog', self.definite_plural))

        irregular = Noun('child', 'children')
        new = irregular.plural().definite()
        self.assertEqual(new, Noun('the children', 'children', 'child', self.definite_plural))

    def test_indefinite_plural(self):
        noun = Noun('dog')
        new = noun.indefinite().plural()
        self.assertEqual(new, Noun('a dogs', '', 'dog', tags=self.plural))

        irregular = Noun('child', 'children')
        new = irregular.indefinite().plural()
        self.assertEqual(new, Noun('a children', 'children', 'child', tags=self.plural))

    def test_plural_indefinite(self):
        noun = Noun('dog')
        new = noun.plural().indefinite()
        self.assertEqual(new, Noun('a dogs', '', 'dog', tags=self.indefinite))

        irregular = Noun('child', 'children')
        new = irregular.plural().indefinite()
        self.assertEqual(new, Noun('a children', 'children', 'child', tags=self.indefinite))

    def test_uncountable_plural(self):
        noun = Noun.uncountable_noun('water')
        self.assertEqual(noun.plural(), Noun('waters', '', 'water', Tags([WordTag.PLURAL])))

    def test_definite_uncountable_plural(self):
        noun = Noun.uncountable_noun('water')
        self.assertEqual(noun.definite().plural(), Noun('the waters', '', 'water', tags=self.definite_plural))

    def test_proper_noun_plural(self):
        noun = Noun.proper_noun('Bob')
        self.assertEqual(noun.plural(), Noun('Bobs', '', 'Bob', tags=self.plural_proper))

    def test_to_basic_noun_keeps_plural_info(self):
        self.assertEqual(Noun('bob', 'boba').to_basic_noun(), Noun('bob', 'boba'))

    def test_to_basic_noun_no_special_plural(self):
        original = Noun('bob')
        self.assertEqual(original.plural().to_basic_noun(), original)
        self.assertEqual(original.bold().to_basic_noun(), original)
        self.assertEqual(original.indefinite().to_basic_noun(), original)
        self.assertEqual(original.definite().to_basic_noun(), original)
        self.assertEqual(original.definite().plural().to_basic_noun(), original)
        self.assertEqual(original.capitalize().plural().definite().to_basic_noun(), original)

    def test_to_basic_noun_special_plural(self):
        original = Noun('bob', 'boberino')
        self.assertEqual(original.plural().to_basic_noun(), original)
        self.assertEqual(original.bold().to_basic_noun(), original)
        self.assertEqual(original.indefinite().to_basic_noun(), original)
        self.assertEqual(original.definite().to_basic_noun(), original)
        self.assertEqual(original.definite().plural().to_basic_noun(), original)
        self.assertEqual(original.capitalize().plural().definite().to_basic_noun(), original)

    def test_to_basic_noun_removes_tags(self):
        original = Noun.proper_noun('the Things', plural=True)
        self.assertTrue(original.has_tags(WordTag.PROPER, WordTag.PLURAL))
        without_tags = Noun('the Things')
        self.assertEqual(original.to_basic_noun(), without_tags)

        original = Noun.uncountable_noun('water')
        self.assertTrue(original.has_tags(WordTag.UNCOUNTABLE))
        without_tags = Noun('water')
        self.assertEqual(original.to_basic_noun(), without_tags)
