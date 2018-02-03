

def bold(word_value) -> str:
    if word_value.endswith('</bold>') and word_value.startswith('<bold>'):
        return word_value
    return '<bold>{}</bold>'.format(word_value)


def add_s(word_value):
    if needs_es(word_value):
        ending = 'es'
    elif is_y_as_long_vowel_sound(word_value):
        word_value = word_value[:-1]
        ending = 'ies'
    else:
        ending = 's'
    return word_value + ending


def add_ed(word_value) -> str:
    if is_y_as_long_vowel_sound(word_value):
        ending = 'ied'
        word_value = word_value[:-1]
    elif word_value.endswith('e'):
        ending = 'd'
    elif ends_with_short_vowel_and_consonant(word_value):
        ending = word_value[-1] + 'ed'
    else:
        ending = 'ed'

    return word_value + ending


def needs_es(value: str):
    add_es = ['s', 'z', 'ch', 'sh', 'x', 'o']
    return any(value.endswith(ending) for ending in add_es)


def is_y_as_long_vowel_sound(value: str) -> bool:
    vowels = 'aeiou '
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





