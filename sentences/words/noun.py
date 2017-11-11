from sentences.words.word import Word


class Noun(Word):
    def __init__(self, word, special_plural=''):
        self._plural = special_plural
        super(Noun, self).__init__(word)

    def indefinite(self) -> 'Noun':
        article = 'a '
        vowels = 'aeiouAEIOU'
        if any(self.value.startswith(vowel) for vowel in vowels):
            article = 'an '
        return IndefiniteNoun(article + self.value, article + self.plural().value)

    def definite(self) -> 'Noun':
        class_ = DefiniteNoun
        if isinstance(self, PluralNoun):
            class_ = DefinitePluralNoun
        article = 'the '
        return class_(article + self.value, article + self.plural().value)

    def plural(self) -> 'Noun':
        class_ = PluralNoun
        if isinstance(self, DefiniteNoun):
            class_ = DefinitePluralNoun
        if self._plural:
            return class_(self._plural)
        return class_(self.add_s().value)
    
    def __eq__(self, other):
        if not isinstance(other, Noun):
            return False
        return self.plural().value == other.plural().value and super(Noun, self).__eq__(other)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.value, self._plural)


class PluralNoun(Noun):
    pass


class DefiniteNoun(Noun):
    pass


class IndefiniteNoun(Noun):
    pass


class DefinitePluralNoun(DefiniteNoun, PluralNoun):
    pass
