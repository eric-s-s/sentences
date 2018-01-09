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
        return super(Verb, self).__eq__(other) and self.infinitive == other.infinitive

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(Verb, self).__hash__()

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.value, self.infinitive)

    def to_basic_verb(self):
        return BasicVerb(self.infinitive)

    def capitalize(self):
        return self.__class__(self.value.capitalize(), self.infinitive)


class ConjugatedVerb(Verb):
    def __init__(self, word, infinitive=''):
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
        if with_s == 'haves':
            with_s = 'has'
        return ConjugatedVerb(with_s, self.value)

    def capitalize(self) -> 'BasicVerb':
        infinitive = self.infinitive
        return BasicVerb(self.value.capitalize(), self._past_tense, infinitive)

    def negative(self) -> 'NegativeVerb':
        return NegativeVerb("don't " + self.value, self.value)

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(self.__class__.__name__, self.value, self._past_tense, self.infinitive)


class NegativeVerb(Verb):
    def __init__(self, negative, infinitive=''):
        super(NegativeVerb, self).__init__(negative, infinitive)

    def past_tense(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'did')
        new_value = new_value.replace('Do', 'did')
        return ConjugatedVerb(new_value, self.infinitive)

    def third_person(self) -> ConjugatedVerb:
        new_value = self.value.replace('do', 'does')
        new_value = new_value.replace('Do', 'does')
        return ConjugatedVerb(new_value, self.infinitive)


class NewVerb(Word):
    def __init__(self, value, infinitive='', irregular_past=''):
        super(NewVerb, self).__init__(value)
        self._irregular_past = irregular_past
        self._inf = infinitive
        if not infinitive:
            self._inf = value

    @property
    def infinitive(self):
        return self._inf

    @property
    def irregular_past(self):
        return self._irregular_past

    def past_tense(self):
        past_tense_value = self._irregular_past
        if not past_tense_value:
            past_tense_value = Word(self._inf).add_ed().value
        return PastVerb(past_tense_value, self._inf, self._irregular_past)

    def third_person(self):
        with_s = Word(self._inf).add_s().value
        if with_s == 'haves':
            with_s = 'has'
        return ThirdPersonVerb(with_s, self._inf, self._irregular_past)

    def capitalize(self):
        class_ = self.__class__
        return class_(self.value.capitalize(), self._inf, self._irregular_past)

    def negative(self):
        return NegVerb("don't " + self.infinitive, self._inf, self._irregular_past)

    def to_base_verb(self):
        return NewVerb(self._inf, '', self._irregular_past)

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(
            self.__class__.__name__, self.value, self._inf, self._irregular_past
        )


class PastVerb(NewVerb):
    def negative(self):
        return NegativePastVerb("didn't " + self.infinitive, self.infinitive, self.irregular_past)


class NegVerb(NewVerb):
    def past_tense(self):
        return NegativePastVerb("didn't " + self.infinitive, self.infinitive, self.irregular_past)

    def third_person(self):
        return NegativeThirdPersonVerb("doesn't " + self.infinitive, self.infinitive, self.irregular_past)


class ThirdPersonVerb(NewVerb):
    def negative(self):
        return NegativeThirdPersonVerb("doesn't " + self.infinitive, self.infinitive, self.irregular_past)


class NegativePastVerb(NegVerb, PastVerb):
    pass


class NegativeThirdPersonVerb(NegVerb, ThirdPersonVerb):
    pass
