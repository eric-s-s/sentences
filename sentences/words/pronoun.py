from enum import Enum

from sentences.words.word import Word


class Pronoun(Enum):
    I = 'I'
    ME = 'me'

    YOU = 'you'

    HE = 'he'
    HIM = 'him'

    SHE = 'she'
    HER = 'her'

    IT = 'it'

    WE = 'we'
    US = 'us'

    THEY = 'they'
    THEM = 'them'

    CAPITAL_ME = 'Me'

    CAPITAL_YOU = 'You'

    CAPITAL_HE = 'He'
    CAPITAL_HIM = 'Him'

    CAPITAL_SHE = 'She'
    CAPITAL_HER = 'Her'

    CAPITAL_IT = 'It'

    CAPITAL_WE = 'We'
    CAPITAL_US = 'Us'

    CAPITAL_THEY = 'They'
    CAPITAL_THEM = 'Them'

    @classmethod
    def lowers(cls):
        return [cls.I, cls.ME, cls.YOU, cls.HE, cls.HIM, cls.SHE, cls.HER, cls.IT, cls.WE, cls.US, cls.THEY, cls.THEM]

    @classmethod
    def uppers(cls):
        return [pronoun.capitalize() for pronoun in cls.lowers()]

    def is_upper_case(self):
        return self.name.startswith('CAPITAL_')

    def capitalize(self):
        if self.is_upper_case():
            return self
        return getattr(self.__class__, 'CAPITAL_{}'.format(self.name))

    def de_capitalize(self):
        return getattr(self.__class__, self.name.replace('CAPITAL_', ''))

    def bold(self):
        return Word(self.value).bold()

    def object(self):
        capitalize = False
        to_test = self
        if self.is_upper_case():
            print('hi', to_test)
            capitalize = True
            to_test = self.de_capitalize()

        changes = {self.I: self.ME,
                   self.HE: self.HIM,
                   self.SHE: self.HER,
                   self.WE: self.US,
                   self.THEY: self.THEM}
        new = to_test
        if to_test in changes:
            new = changes[to_test]
        if capitalize:
            new = new.capitalize()
        return new

    def subject(self):
        changes = {self.ME: self.I,
                   self.HIM: self.HE,
                   self.HER: self.SHE,
                   self.US: self.WE,
                   self.THEM: self.THEY}
        if self in changes:
            return changes[self]
        return self

    def is_pair(self, other):
        if not isinstance(other, Pronoun):
            return False
        return self.subject() == other.subject()
