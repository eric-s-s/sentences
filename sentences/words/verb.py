from sentences.words.word import Word


class Verb(Word):
    def __init__(self, word):
        super(Verb, self).__init__(word)

    @property
    def infinitive(self) -> str:
        return self.value

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return False
        return (self.value, self.infinitive) == (other.value, other.infinitive)

    def __ne__(self, other):
        return not self.__eq__(other)


class ConjugatedVerb(Verb):
    def __init__(self, word, infinitive):
        self._inf = infinitive
        super(ConjugatedVerb, self).__init__(word)

    @property
    def infinitive(self) -> str:
        return self._inf

    def __repr__(self):
        return 'ConjugatedVerb({!r}, {!r})'.format(self.value, self.infinitive)


class BasicVerb(Verb):
    def __init__(self, word, special_past_tense=''):
        self._past_tense = special_past_tense
        super(BasicVerb, self).__init__(word)

    def past_tense(self) -> ConjugatedVerb:
        past_tense_value = self._past_tense
        if not past_tense_value:
            past_tense_value = self.add_ed().value

        return ConjugatedVerb(past_tense_value, self.value)

    def third_person(self) -> ConjugatedVerb:
        with_s = self.add_s().value
        return ConjugatedVerb(with_s, self.value)

    def negative(self) -> 'NegativeVerb':
        return NegativeVerb(self.value)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.value, self._past_tense)


class NegativeVerb(Verb):
    def __init__(self, infinitive):
        super(NegativeVerb, self).__init__(infinitive)

    @property
    def value(self):
        return 'don\'t ' + super(NegativeVerb, self).value

    @property
    def infinitive(self):
        return super(NegativeVerb, self).value

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.infinitive)

    def past_tense(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'did')
        return ConjugatedVerb(new_value, self.infinitive)

    def third_person(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'does')
        return ConjugatedVerb(new_value, self.infinitive)
