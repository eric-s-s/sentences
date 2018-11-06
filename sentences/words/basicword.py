from sentences.words.wordtools.abstractword import AbstractWord
from sentences.tags.tags import Tags
from sentences.tags.wordtag import WordTag
from sentences.words.wordtools.common_functions import bold


class BasicWord(AbstractWord):
    def __init__(self, value, tags=None):
        self._value = value
        if tags is None:
            tags = Tags()
        self._tags = tags

    @classmethod
    def preposition(cls, value):
        return cls(value, Tags([WordTag.PREPOSITION]))

    @classmethod
    def particle(cls, value):
        return cls(value, Tags([WordTag.SEPARABLE_PARTICLE]))

    @property
    def value(self):
        return self._value

    @property
    def tags(self):
        return self._tags.copy()

    def capitalize(self):
        new_value = self.value[0].upper() + self.value[1:]
        return BasicWord(new_value, self.tags)

    def de_capitalize(self):
        new_value = self.value[0].lower() + self.value[1:]
        return BasicWord(new_value, self.tags)

    def bold(self):
        return BasicWord(bold(self.value), self.tags)

    def __repr__(self):
        return '{}({!r}, {!r})'.format(self.__class__.__name__, self.value, self.tags)

    def __hash__(self):
        return hash('hash of {!r}'.format(self))

    def __eq__(self, other):
        if not isinstance(other, BasicWord):
            return False
        return (self.value, self.tags) == (other.value, other.tags)
