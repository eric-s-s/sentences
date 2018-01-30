from sentences.words.word import Word


class Noun(Word):
    def __init__(self, word, irregular_plural='', base=''):
        self._irregular = irregular_plural
        super(Noun, self).__init__(word)
        self._base_noun = base
        if self._base_noun == '':
            self._base_noun = word

    @property
    def base_noun(self):
        return self._base_noun

    @property
    def irregular_plural(self):
        return self._irregular

    def capitalize(self):
        value = self.value[0].upper() + self.value[1:]
        return self.__class__(value, self.irregular_plural, self.base_noun)

    def de_capitalize(self):
        value = self.value[0].lower() + self.value[1:]
        return self.__class__(value, self.irregular_plural, self.base_noun)

    def indefinite(self) -> 'Noun':
        article = 'a '
        vowels = 'aeiouAEIOU'
        if any(self.value.startswith(vowel) for vowel in vowels):
            article = 'an '
        return IndefiniteNoun(article + self.value, self.irregular_plural, self.base_noun)

    def definite(self) -> 'Noun':
        return DefiniteNoun('the ' + self.value, self.irregular_plural, self.base_noun)

    def plural(self) -> 'Noun':
        if self.irregular_plural:
            return PluralNoun(self.irregular_plural, self.irregular_plural, base=self.base_noun)
        return PluralNoun(get_plural_value(self), base=self.base_noun)

    def to_base_noun(self) -> 'Noun':
        return Noun(self.base_noun, self.irregular_plural)
    
    def __eq__(self, other):
        return (super(Noun, self).__eq__(other) and
                (self.irregular_plural, self.base_noun) == (other.irregular_plural, other.base_noun))

    def __hash__(self):
        return super(Noun, self).__hash__()

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(self.__class__.__name__, self.value, self.irregular_plural, self.base_noun)


class PluralNoun(Noun):
    def definite(self):
        return DefinitePluralNoun('the ' + self.value, self.irregular_plural, self.base_noun)


class DefiniteNoun(Noun):
    def plural(self):
        plural_val = 'the ' + self.irregular_plural
        if plural_val == 'the ':
            plural_val = get_plural_value(self)
        return DefinitePluralNoun(plural_val, self.irregular_plural, self.base_noun)


class IndefiniteNoun(Noun):
    def plural(self):
        if self.irregular_plural:
            article = self.value.split(' ')[0]
            plural_val = '{} {}'.format(article, self.irregular_plural)
        else:
            plural_val = get_plural_value(self)
        return PluralNoun(plural_val, self.irregular_plural, self.base_noun)


class DefinitePluralNoun(DefiniteNoun, PluralNoun):
    pass


class UncountableNoun(Noun):
    def definite(self):
        return DefiniteUncountableNoun('the ' + self.value, self.irregular_plural, self.base_noun)


class DefiniteUncountableNoun(UncountableNoun, DefiniteNoun):
    pass


class ProperNoun(Noun):
    def plural(self):
        return PluralProperNoun(get_plural_value(self), self.irregular_plural, self.base_noun)

    def to_base_noun(self):
        return self.__class__(self.base_noun, self.irregular_plural)

    def de_capitalize(self):
        new_val = self.value
        if not new_val.startswith(self.base_noun):
            new_val = new_val[0].lower() + new_val[1:]
        return self.__class__(new_val, self.irregular_plural, self.base_noun)

    def _is_base_lower(self):
        return self.base_noun[0].islower()


class PluralProperNoun(ProperNoun, PluralNoun):
    def plural(self):
        return self


def get_plural_value(noun):
    value = noun.value
    if value.endswith('ife'):
        return value[:-3] + 'ives'
    elif any(value.endswith('{}f'.format(ending)) for ending in ('al', 'el', 'ar', 'ea', 'ol')):
        return value[:-1] + 'ves'
    else:
        return noun.add_s().value
