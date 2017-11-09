

class Word(object):

    def __init__(self, word: str) -> None:
        self._word = word.strip()

    @property
    def value(self) -> str:
        return self._word

    def capitalize(self) -> 'Word':
        return self.__class__(self.value.capitalize())

    def add_s(self) -> 'Word':
        current_value = self.value
        if needs_es(current_value):
            ending = 'es'
        elif is_y_as_long_vowel_sound(current_value):
            current_value = current_value[:-1]
            ending = 'ies'
        elif current_value.endswith('lf'):
            current_value = current_value[:-2]
            ending = 'lves'
        else:
            ending = 's'
        return self.__class__(current_value + ending)

    def add_ed(self) -> 'Word':
        current_value = self.value
        if is_y_as_long_vowel_sound(current_value):
            ending = 'ied'
            current_value = current_value[:-1]
        elif current_value.endswith('e'):
            ending = 'd'
        elif ends_with_short_vowel_and_consonant(current_value):
            ending = current_value[-1] + 'ed'
        else:
            ending = 'ed'

        return self.__class__(current_value + ending)

    def __str__(self):
        return self.value

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.value)

    def __hash__(self):
        return hash('hash of {!r}'.format(self))

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.value == other.value

    def __lt__(self, other):
        return self.value.__lt__(other.value)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other


def needs_es(value: str):
    add_es = ['s', 'z', 'ch', 'sh', 'x']
    return any(value.endswith(ending) for ending in add_es)


def is_y_as_long_vowel_sound(value: str) -> bool:
    vowels = 'aeiou'
    return value.endswith('y') and len(value) > 1 and value[-2] not in vowels


def ends_with_short_vowel_and_consonant(value: str) -> bool:
    vowels = 'aeiou'
    vowels_plus = vowels + 'wy'

    word_len = len(value)
    if word_len > 1 and value[-2] in vowels and value[-1] not in vowels_plus:
        if word_len > 2:
            return value[-3] not in vowels
        return True
    return False


