from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.wordtools.common_functions import add_s, bold
from sentences.tags.wordtag import WordTag
from sentences.tags.tags import Tags


class Noun(AbstractWord):
    def __init__(self, value, irregular_plural='', base='', tags=None):
        self._value = value
        self._irregular = irregular_plural
        if not base:
            base = value
        self._base = base

        if not tags:
            tags = Tags()
        self._tags = tags.copy()

    @classmethod
    def uncountable_noun(cls, value):
        return cls(value, '', '', Tags([WordTag.UNCOUNTABLE]))

    @classmethod
    def proper_noun(cls, value, plural=False):
        tags = Tags([WordTag.PROPER])
        if plural:
            tags = tags.add(WordTag.PLURAL)
        return cls(value, '', '', tags)

    @property
    def value(self):
        return self._value

    @property
    def irregular_plural(self):
        return self._irregular

    @property
    def base_noun(self):
        return self._base

    @property
    def tags(self):
        return self._tags.copy()

    def __eq__(self, other):
        if not isinstance(other, Noun):
            return False
        return ((self.value, self.irregular_plural, self.base_noun, self.tags) ==
                (other.value, other.irregular_plural, other.base_noun, other.tags))

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(
            self.__class__.__name__, self.value, self.irregular_plural, self.base_noun, self.tags
        )

    def __hash__(self):
        return hash('hash of {!r}'.format(self))

    def capitalize(self) -> 'Noun':
        new_value = self.value[0].upper() + self.value[1:]
        return Noun(new_value, self.irregular_plural, self.base_noun, self.tags)

    def de_capitalize(self) -> 'Noun':
        if self.value.startswith(self.base_noun):
            return self

        new_value = self.value[0].lower() + self.value[1:]
        return Noun(new_value, self.irregular_plural, self.base_noun, self.tags)

    def bold(self) -> 'Noun':
        return Noun(bold(self.value), self.irregular_plural, self.base_noun, self.tags)

    def definite(self):
        if self.has_tags(WordTag.DEFINITE):
            return self
        new_value = 'the ' + self.value
        new_tags = self.tags.add(WordTag.DEFINITE).remove(WordTag.INDEFINITE).remove(WordTag.PROPER)
        return Noun(new_value, self.irregular_plural, self.base_noun, new_tags)

    def indefinite(self):
        if self.has_tags(WordTag.INDEFINITE):
            return self
        article = 'a '
        if any(self.value.startswith(vowel) for vowel in 'aeiouAEIOU'):
            article = 'an '
        return Noun(article + self.value, self.irregular_plural, self.base_noun, Tags([WordTag.INDEFINITE]))

    def plural(self):
        if self.has_tags(WordTag.PLURAL):
            return self

        new_tags = self.tags.add(WordTag.PLURAL).remove(WordTag.INDEFINITE).remove(WordTag.UNCOUNTABLE)
        if not self.irregular_plural:
            return Noun(get_plural_value(self.value), self.irregular_plural, self.base_noun, new_tags)

        new_value = get_article(self.value) + self.irregular_plural
        return Noun(new_value, self.irregular_plural, self.base_noun, new_tags)

    def to_basic_noun(self):
        tags = []
        if self.has_tags(WordTag.UNCOUNTABLE):
            tags.append(WordTag.UNCOUNTABLE)
        if self.has_tags(WordTag.PROPER):
            tags.append(WordTag.PROPER)
        if self.has_tags(WordTag.PROPER, WordTag.PLURAL):
            tags.append(WordTag.PLURAL)
        return Noun(self.base_noun, self.irregular_plural, tags=Tags(tags))


def get_plural_value(value):
    if value.endswith('ife'):
        return value[:-3] + 'ives'
    elif any(value.endswith('{}f'.format(ending)) for ending in ('al', 'el', 'ar', 'ea', 'ol')):
        return value[:-1] + 'ves'
    else:
        return add_s(value)


def get_article(value):
    articles = ['The ', 'the ', 'A ', 'a ', 'An ', 'an ']
    for article in articles:
        if value.startswith(article):
            return article
    return ''
