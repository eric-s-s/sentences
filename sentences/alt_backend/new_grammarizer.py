from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag
from sentences.word_groups.paragraph import Paragraph
from sentences.word_groups.sentence import Sentence
from sentences.words.noun import Noun
from sentences.words.pronoun import Pronoun


class NewGrammarizer(object):
    def __init__(self, raw_paragraph: Paragraph):
        self._raw = raw_paragraph
        self._altered = None  # type: Paragraph

    @property
    def raw(self):
        return self._raw

    def grammarize_to_present_tense(self):
        self._altered = self._raw
        self._assign_noun_articles()
        self._assign_present_tense_verbs()
        return self._set_tags()

    def grammarize_to_past_tense(self):
        self._altered = self._raw
        self._assign_noun_articles()
        return self._set_tags()

    def _assign_present_tense_verbs(self):
        for s_index, sentence in enumerate(self._altered):  # type: Sentence
            v_index = sentence.get_verb()
            if _needs_third_person(sentence):
                new_verb = sentence.get(v_index).third_person()
                new_sentence = sentence.set(v_index, new_verb)
                self._altered = self._altered.set_sentence(s_index, new_sentence)

    def _assign_past_tense_verbs(self):
        pass

    def _assign_noun_articles(self):
        assign_definite = set()
        for s_index, w_index, word in self._altered.indexed_all_words():
            if _is_alterable_noun(word):
                if word in assign_definite:
                    self._altered = self._altered.set(s_index, w_index, word.definite())  # type: Paragraph
                else:
                    new_word = word if word.has_tags(WordTag.PLURAL) else word.indefinite()
                    self._altered = self._altered.set(s_index, w_index, new_word)
                    assign_definite.add(word)

    def _set_tags(self):
        return self._altered.set_tags(self._raw.tags.add(StatusTag.GRAMMATICAL).remove(StatusTag.RAW))


def _is_alterable_noun(word):
    uncountable_ = isinstance(word, Noun) and not (
            word.has_tags(WordTag.PROPER) or word.has_tags(WordTag.UNCOUNTABLE))
    return uncountable_


def _needs_third_person(sentence: Sentence):
    verb_index = sentence.get_verb()
    subject_index = sentence.get_subject()
    if verb_index == -1 or subject_index == -1:
        return False

    subject = sentence.get(subject_index)

    third_person_pronouns = (Pronoun.HE, Pronoun.SHE, Pronoun.IT)
    if isinstance(subject, Pronoun) and subject not in third_person_pronouns:
        return False
    return not subject.has_tags(WordTag.PLURAL)
