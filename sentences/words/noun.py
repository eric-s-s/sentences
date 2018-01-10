from sentences.words.word import Word


class Noun(Word):
    def __init__(self, word: str, irregular_plural: str= '', base: str = None):
        self._plural = irregular_plural
        super(Noun, self).__init__(word)
        self._base_noun = base
        if self._base_noun is None:
            self._base_noun = word

    @property
    def base_noun(self):
        return self._base_noun

    def capitalize(self):
        value = super(Noun, self).capitalize().value
        return self.__class__(value, self._plural, self.base_noun)

    def indefinite(self) -> 'Noun':
        article = 'a '
        vowels = 'aeiouAEIOU'
        if any(self.value.startswith(vowel) for vowel in vowels):
            article = 'an '
        return IndefiniteNoun(article + self.value, article + self.plural().value, self.base_noun)

    def definite(self) -> 'Noun':
        class_ = _get_definite_class(self)

        article = 'the '
        return class_(article + self.value, article + self.plural().value, self.base_noun)

    def plural(self) -> 'Noun':
        class_ = _get_plural_class(self)

        if self._plural:
            return class_(self._plural, base=self.base_noun)
        current = self.value
        if any(current.endswith('{}fe'.format(vowel)) for vowel in 'aeiou'):
            plural_val = current[:-2] + 'ves'
        elif any(current.endswith('{}f'.format(vowel)) for vowel in 'al'):
            plural_val = current[:-1] + 'ves'
        else:
            plural_val = self.add_s().value

        return class_(plural_val, base=self.base_noun)

    def to_base_noun(self) -> 'Noun':
        return Noun(self.base_noun)
    
    def __eq__(self, other):
        return super(Noun, self).__eq__(other) and self.base_noun == other.base_noun

    def __hash__(self):
        return super(Noun, self).__hash__()

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(self.__class__.__name__, self.value, self._plural, self.base_noun)


class PluralNoun(Noun):
    pass


class DefiniteNoun(Noun):
    pass


class IndefiniteNoun(Noun):
    pass


class DefinitePluralNoun(DefiniteNoun, PluralNoun):
    pass


class UncountableNoun(Noun):
    pass


class DefiniteUncountableNoun(UncountableNoun, DefiniteNoun):
    pass


def _get_definite_class(noun):
    current_class = noun.__class__
    if isinstance(noun, DefiniteNoun):
        return current_class
    to_definite = {
        UncountableNoun: DefiniteUncountableNoun,
        PluralNoun: DefinitePluralNoun,

    }
    return to_definite.get(current_class, DefiniteNoun)


def _get_plural_class(noun):
    if isinstance(noun, DefiniteNoun):
        return DefinitePluralNoun
    return PluralNoun
