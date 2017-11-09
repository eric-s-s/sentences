from sentences.words.word import Word


class Verb(Word):
    def __init__(self, word):
        super(Verb, self).__init__(word)

    @property
    def infinitive(self):
        return self.value


class ConjugatedVerb(Verb):
    def __init__(self, word, infinitive):
        self._inf = infinitive
        super(ConjugatedVerb, self).__init__(word)

    @property
    def infinitive(self):
        return self._inf


class ConjugatableVerb(Verb):
    def __init__(self, word, special_past_tense=''):
        self._past_tense = special_past_tense
        super(ConjugatableVerb, self).__init__(word)

    def past_tense(self):
        if self._past_tense:
            past_tense_value = self._past_tense
        else:
            past_tense_value = self.add_ed().value

        return ConjugatedVerb(past_tense_value, self.value)

    def third_person(self):
        with_s = self.add_s().value
        return ConjugatedVerb(with_s, self.value)
