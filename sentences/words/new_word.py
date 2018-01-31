from sentences.words.wordtag import WordTag as wt


class Tags(object):
    def __init__(self, types_list=None):
        self._types = set()
        if types_list:
            self._types = {word_type for word_type in types_list}

    def to_list(self):
        return sorted(self._types)

    def add(self, new_type):
        new_val = self.to_list()
        new_val.append(new_type)
        return Tags(new_val)

        # self._types.add(new_type)

    def remove(self, type_):
        new_val = self._types.copy()
        new_val.discard(type_)
        return Tags(list(new_val))
        # self._types.discard(type_)

    def has(self, type_):
        return type_ in self._types

    def copy(self):
        return Tags(self.to_list())

    def __eq__(self, other):
        if not isinstance(other, Tags):
            return False
        return self.to_list() == other.to_list()

    def __repr__(self):
        return 'Tags({})'.format([tag.name for tag in self.to_list()])


class WordValues(object):
    def __init__(self, value, irregular='', base=''):
        if not base:
            base = value
        self._value = value
        self._base = base
        self._irregular = irregular

    @property
    def value(self):
        return self._value

    @property
    def irregular(self):
        return self._irregular

    @property
    def base(self):
        return self._base

    def bold(self):
        return WordValues('<bold>{}</bold>'.format(self.value), self.irregular, self.base)


class NewNoun(object):
    def __init__(self, value, irregular_plural='', base='', word_types=None):
        self._values = WordValues(value, irregular_plural, base)
        if not word_types:
            word_types = Tags()
        self._types = word_types.copy()

    @classmethod
    def uncountable_noun(cls, value):
        return cls(value, '', '', Tags([wt.UNCOUNTABLE]))

    @classmethod
    def proper_noun(cls, value, plural=False):
        types = Tags([wt.PROPER])
        if plural:
            types = types.add(wt.PLURAL)
        return cls(value, '', '', types)

    @property
    def value(self):
        return self._values.value

    @property
    def irregular_plural(self):
        return self._values.irregular

    @property
    def base_noun(self):
        return self._values.base

    @property
    def tags(self):
        return self._types.copy()

    def __eq__(self, other):
        if not isinstance(other, NewNoun):
            return False
        return ((self.value, self.irregular_plural, self.base_noun, self.tags) ==
                (other.value, other.irregular_plural, other.base_noun, other.tags))

    def __repr__(self):
        return 'NewNoun({!r}, {!r}, {!r}, {!r})'.format(self.value, self.irregular_plural, self.base_noun, self.tags)

    def is_types(self, *types):
        return all(self._types.has(type_) for type_ in types)

    def definite(self):
        new_value = 'the ' + self.value
        new_tags = self.tags.add(wt.DEFINITE)
        return NewNoun(new_value, self.irregular_plural, self.base_noun, new_tags)

    def capitalize(self):
        new_value = self.value[0].upper() + self.value[1:]
        return NewNoun(new_value, self.irregular_plural, self.base_noun, self.tags)

    def indefinite(self):
        article = 'a '
        vowels = 'aeiouAEIOU'
        if any(self.value.startswith(vowel) for vowel in vowels):
            article = 'an '
        return NewNoun(article + self.value, self.irregular_plural, self.base_noun, Tags([wt.INDEFINITE]))

    def plural(self):
        new_value = self.irregular_plural
        new_tags = self.tags.add(wt.PLURAL)
        if not new_value:
            new_value = get_plural_value(self.value)
        return NewNoun(new_value, self.irregular_plural, self.base_noun, new_tags)


def get_plural_value(value):
    if value.endswith('ife'):
        return value[:-3] + 'ives'
    elif any(value.endswith('{}f'.format(ending)) for ending in ('al', 'el', 'ar', 'ea', 'ol')):
        return value[:-1] + 'ves'
    else:
        return add_s(value)


def add_s(word_value):
    if needs_es(word_value):
        ending = 'es'
    elif is_y_as_long_vowel_sound(word_value):
        word_value = word_value[:-1]
        ending = 'ies'
    else:
        ending = 's'
    return word_value + ending


def needs_es(value: str):
    add_es = ['s', 'z', 'ch', 'sh', 'x', 'o']
    return any(value.endswith(ending) for ending in add_es)


def is_y_as_long_vowel_sound(value: str) -> bool:
    vowels = 'aeiou '
    return value.endswith('y') and len(value) > 1 and value[-2] not in vowels


