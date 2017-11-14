from sentences.words.word import Word


class Noun(Word):
    def __init__(self, word: str, special_plural: str='', base: str = None):
        self._plural = special_plural
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
        class_ = DefiniteNoun
        if isinstance(self, PluralNoun):
            class_ = DefinitePluralNoun
        article = 'the '
        return class_(article + self.value, article + self.plural().value, self.base_noun)

    def plural(self) -> 'Noun':
        class_ = PluralNoun
        if isinstance(self, DefiniteNoun):
            class_ = DefinitePluralNoun

        if self._plural:
            return class_(self._plural, base=self.base_noun)
        current = self.value
        if any(current.endswith('{}fe'.format(vowel)) for vowel in 'aeiou'):
            plural_val = current[:-2] + 'ves'
        else:
            plural_val = self.add_s().value

        return class_(plural_val, base=self.base_noun)

    def revert(self) -> 'Noun':
        return Noun(self.base_noun)
    
    def __eq__(self, other):
        if not isinstance(other, Noun):
            return False
        return self.base_noun == other.base_noun and super(Noun, self).__eq__(other)

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
