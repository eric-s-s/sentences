from sentences.words.word import Word


class Verb(Word):
    def __init__(self, value, irregular_past='', infinitive=''):
        super(Verb, self).__init__(value)
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

    def add_ed(self):
        value = super(Verb, self).add_ed().value
        return self.__class__(value, self.irregular_past, self.infinitive)

    def add_s(self):
        value = super(Verb, self).add_s().value
        return self.__class__(value, self.irregular_past, self.infinitive)

    def past_tense(self):
        past_tense_value = self.irregular_past
        if not past_tense_value:
            past_tense_value = Word(self.infinitive).add_ed().value
        return PastVerb(past_tense_value, self.irregular_past, self.infinitive)

    def third_person(self):
        with_s = Word(self.infinitive).add_s().value
        if with_s == 'haves':
            with_s = 'has'
        return ThirdPersonVerb(with_s, self.irregular_past, self.infinitive)

    def capitalize(self):
        class_ = self.__class__
        return class_(self.value.capitalize(), self.irregular_past, self.infinitive)

    def negative(self):
        return NegativeVerb("don't " + self.infinitive, self.irregular_past, self.infinitive)

    def to_base_verb(self):
        return Verb(self.infinitive, self.irregular_past, '')

    def __repr__(self):
        return '{}({!r}, {!r}, {!r})'.format(
            self.__class__.__name__, self.value, self.irregular_past, self.infinitive
        )

    def __eq__(self, other):
        return (super(Verb, self).__eq__(other) and
                (self.infinitive, self.irregular_past) == (other.infinitive, other.irregular_past))

    def __hash__(self):
        return super(Verb, self).__hash__()


class PastVerb(Verb):
    def negative(self):
        return NegativePastVerb("didn't " + self.infinitive, self.irregular_past, self.infinitive)


class NegativeVerb(Verb):
    def past_tense(self):
        return NegativePastVerb("didn't " + self.infinitive, self.irregular_past, self.infinitive)

    def third_person(self):
        return NegativeThirdPersonVerb("doesn't " + self.infinitive, self.irregular_past, self.infinitive)


class ThirdPersonVerb(Verb):
    def negative(self):
        return NegativeThirdPersonVerb("doesn't " + self.infinitive, self.irregular_past, self.infinitive)


class NegativePastVerb(NegativeVerb, PastVerb):
    pass


class NegativeThirdPersonVerb(NegativeVerb, ThirdPersonVerb):
    pass
