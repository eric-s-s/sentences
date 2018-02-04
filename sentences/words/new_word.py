from sentences.words.wordtools.abstractword import AbstractWord
from sentences.words.wordtools.common_functions import add_s, bold
from sentences.words.wordtools.wordtag import WordTag as wt
from sentences.words.wordtools.tags import Tags


class NewNoun(AbstractWord):
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
        return cls(value, '', '', Tags([wt.UNCOUNTABLE]))

    @classmethod
    def proper_noun(cls, value, plural=False):
        tags = Tags([wt.PROPER])
        if plural:
            tags = tags.add(wt.PLURAL)
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
        if not isinstance(other, NewNoun):
            return False
        return ((self.value, self.irregular_plural, self.base_noun, self.tags) ==
                (other.value, other.irregular_plural, other.base_noun, other.tags))

    def __repr__(self):
        return 'NewNoun({!r}, {!r}, {!r}, {!r})'.format(self.value, self.irregular_plural, self.base_noun, self.tags)

    def __hash__(self):
        return hash('hash of {!r}'.format(self))

    def capitalize(self):
        new_value = self.value[0].upper() + self.value[1:]
        return NewNoun(new_value, self.irregular_plural, self.base_noun, self.tags)

    def de_capitalize(self):
        if self.value.startswith(self.base_noun):
            return self

        new_value = self.value[0].lower() + self.value[1:]
        return NewNoun(new_value, self.irregular_plural, self.base_noun, self.tags)

    def bold(self):
        return NewNoun(bold(self.value), self.irregular_plural, self.base_noun, self.tags)

    def definite(self):
        if self.has_tags(wt.DEFINITE):
            return self
        new_value = 'the ' + self.value
        new_tags = self.tags.add(wt.DEFINITE).remove(wt.INDEFINITE).remove(wt.PROPER)
        return NewNoun(new_value, self.irregular_plural, self.base_noun, new_tags)

    def indefinite(self):
        if self.has_tags(wt.INDEFINITE):
            return self
        article = 'a '
        vowels = 'aeiouAEIOU'
        if any(self.value.startswith(vowel) for vowel in vowels):
            article = 'an '
        return NewNoun(article + self.value, self.irregular_plural, self.base_noun, Tags([wt.INDEFINITE]))

    def plural(self):
        if self.has_tags(wt.PLURAL):
            return self
        new_value = self.irregular_plural
        new_tags = self.tags.add(wt.PLURAL).remove(wt.INDEFINITE).remove(wt.UNCOUNTABLE)
        if not new_value:
            return NewNoun(get_plural_value(self.value), self.irregular_plural, self.base_noun, new_tags)

        # if self.has_tags(wt.INDEFINITE) or self.has_tags(wt.DEFINITE):
        new_value = get_article(self.value) + new_value
        return NewNoun(new_value, self.irregular_plural, self.base_noun, new_tags)

    def to_base_noun(self):
        proper = Tags([wt.PROPER])
        plural_proper = Tags([wt.PROPER, wt.PLURAL])
        uncountable = Tags([wt.UNCOUNTABLE])
        tags = Tags()
        for tag_to_preserve in (plural_proper, proper, uncountable):
            if self.has_tags(*tag_to_preserve.to_list()):
                tags = tag_to_preserve
                break
        return NewNoun(self.base_noun, self.irregular_plural, tags=tags)


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
