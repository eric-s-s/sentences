from sentences.words.word import Word


class Verb(Word):
    def __init__(self, word, infinitive=''):
        super(Verb, self).__init__(word)
        self._inf = infinitive
        if not self._inf:
            self._inf = word

    @property
    def infinitive(self) -> str:
        return self._inf

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return False
        return (self.value, self.infinitive) == (other.value, other.infinitive)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.value, self.infinitive)

    def to_basic_verb(self):
        return BasicVerb(self.infinitive)

    def capitalize(self):
        return self.__class__(self.value.capitalize(), self.infinitive)

    def de_capitalize(self):
        new_value = Word(self.value).de_capitalize().value
        return self.__class__(new_value, self.infinitive)


class ConjugatedVerb(Verb):
    def __init__(self, word, infinitive):
        super(ConjugatedVerb, self).__init__(word, infinitive)


class BasicVerb(Verb):
    def __init__(self, word, special_past_tense='', infinitive=''):
        self._past_tense = special_past_tense
        super(BasicVerb, self).__init__(word, infinitive)

    def past_tense(self) -> ConjugatedVerb:
        past_tense_value = self._past_tense
        if not past_tense_value:
            past_tense_value = self.add_ed().value

        return ConjugatedVerb(past_tense_value, self.infinitive)

    def third_person(self) -> ConjugatedVerb:
        with_s = self.add_s().value
        return ConjugatedVerb(with_s, self.value)

    def capitalize(self) -> 'BasicVerb':
        infinitive = self.infinitive
        return BasicVerb(self.value.capitalize(), self._past_tense, infinitive)

    def negative(self) -> 'NegativeVerb':
        return NegativeVerb("don't " + self.value, self.value)

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(self.__class__.__name__, self.value, self._past_tense, self.infinitive)


class NegativeVerb(Verb):
    def __init__(self, negative, infinitive):
        super(NegativeVerb, self).__init__(negative, infinitive)

    def past_tense(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'did')
        new_value = new_value.replace('Do', 'did')
        return ConjugatedVerb(new_value, self.infinitive)

    def third_person(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'does')
        new_value = new_value.replace('Do', 'does')
        return ConjugatedVerb(new_value, self.infinitive)
