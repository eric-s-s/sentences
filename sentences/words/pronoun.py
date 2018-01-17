from enum import Enum

from sentences.words.word import Word


class AbstractPronoun(Enum):
    def capitalize(self):
        raise NotImplementedError

    def de_capitalize(self):
        raise NotImplementedError

    def bold(self):
        return Word(self.value).bold()

    def object(self):
        changes = {self.I: self.ME,
                   self.HE: self.HIM,
                   self.SHE: self.HER,
                   self.WE: self.US,
                   self.THEY: self.THEM}
        if self in changes:
            return changes[self]
        return self

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
        if not isinstance(other, AbstractPronoun):
            return False
        return self.subject() == other.subject()


class Pronoun(AbstractPronoun):
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

    def capitalize(self):
        return getattr(CapitalPronoun, self.name)

    def de_capitalize(self):
        return self


class CapitalPronoun(AbstractPronoun):
    I = 'I'
    ME = 'Me'

    YOU = 'You'

    HE = 'He'
    HIM = 'Him'

    SHE = 'She'
    HER = 'Her'

    IT = 'It'

    WE = 'We'
    US = 'Us'

    THEY = 'They'
    THEM = 'Them'

    def capitalize(self):
        return self

    def de_capitalize(self):
        return getattr(Pronoun, self.name)
