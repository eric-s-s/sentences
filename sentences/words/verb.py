from sentences.words.wordtools.abstractword import AbstractWord
from sentences.tags.tags import Tags
from sentences.tags.wordtag import WordTag
from sentences.words.wordtools.common_functions import add_s, add_ed, bold


class Verb(AbstractWord):
    def __init__(self, value, irregular_past='', infinitive='', tags=None):
        self._value = value
        self._irregular_past = irregular_past
        if not infinitive:
            infinitive = value
        self._inf = infinitive

        if tags is None:
            tags = Tags()
        self._tags = tags.copy()

    @property
    def value(self):
        return self._value

    @property
    def infinitive(self):
        return self._inf

    @property
    def irregular_past(self):
        return self._irregular_past

    @property
    def tags(self):
        return self._tags.copy()

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return False
        return ((self.value, self.irregular_past, self.infinitive, self.tags) ==
                (other.value, other.irregular_past, other.infinitive, other.tags))

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(
            self.__class__.__name__, self.value, self.irregular_past, self.infinitive, self.tags
        )

    def __hash__(self):
        return hash('hash of {!r}'.format(self))

    def capitalize(self) -> 'Verb':
        new_value = self.value[0].upper() + self.value[1:]
        return Verb(new_value, self.irregular_past, self.infinitive, self.tags)

    def de_capitalize(self) -> 'Verb':
        new_value = self.value[0].lower() + self.value[1:]
        return Verb(new_value, self.irregular_past, self.infinitive, self.tags)

    def bold(self) -> 'Verb':
        return Verb(bold(self.value), self.irregular_past, self.infinitive, self.tags)

    def past_tense(self):
        if self.has_tags(WordTag.PAST):
            return self

        new_tags = self.tags.add(WordTag.PAST).remove(WordTag.THIRD_PERSON)
        if self.has_tags(WordTag.NEGATIVE):
            return Verb("didn't " + self.infinitive, self.irregular_past, self.infinitive, new_tags)

        past_tense_value = self.irregular_past
        if not past_tense_value:
            past_tense_value = add_ed(self.infinitive)
        return Verb(past_tense_value, self.irregular_past, self.infinitive, new_tags)

    def third_person(self):
        if self.has_tags(WordTag.THIRD_PERSON):
            return self

        new_tags = self.tags.add(WordTag.THIRD_PERSON).remove(WordTag.PAST)
        if self.has_tags(WordTag.NEGATIVE):
            return Verb("doesn't " + self.infinitive, self.irregular_past, self.infinitive, new_tags)

        with_s = add_s(self.infinitive)
        if with_s == 'haves':
            with_s = 'has'
        return Verb(with_s, self.irregular_past, self.infinitive, new_tags)

    def negative(self):
        if self.has_tags(WordTag.NEGATIVE):
            return self
        new_tags = self.tags.add(WordTag.NEGATIVE)
        negative = "don't "
        if self.has_tags(WordTag.THIRD_PERSON):
            negative = "doesn't "
        if self.has_tags(WordTag.PAST):
            negative = "didn't "
        return Verb(negative + self.infinitive, self.irregular_past, self.infinitive, new_tags)

    def to_basic_verb(self):
        return Verb(self.infinitive, self.irregular_past)
