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

    def capitalize(self):
        return Word(self.value.capitalize())

    def de_capitalize(self):
        return self.capitalize().de_capitalize()

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


