from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.backend.random_assignments.plurals_assignement import get_countable_nouns, PluralsAssignment
from sentences.tags.status_tag import StatusTag
from sentences.tags.wordtag import WordTag
from sentences.words.verb import Verb


def create_answer_paragraph(paragraph_str, base_paragraph):
    plurals_assigned_with_no_articles = _get_plurals_paragraph(base_paragraph, paragraph_str)
    verbs_have_negatives_but_no_grammar = _revert_verbs(plurals_assigned_with_no_articles)
    grammarizer = NewGrammarizer(verbs_have_negatives_but_no_grammar)
    if base_paragraph.tags.has(StatusTag.SIMPLE_PAST):
        answer = grammarizer.grammarize_to_past_tense()
    else:
        answer = grammarizer.grammarize_to_present_tense()
    return answer


def _get_plurals_paragraph(base_paragraph, paragraph_str):
    countable_nouns = get_countable_nouns(base_paragraph)
    plurals = [noun for noun in countable_nouns if noun.plural().value.lower() in paragraph_str.lower()]
    new_base = PluralsAssignment(base_paragraph).assign_plural(plurals)
    return new_base


def _revert_verbs(paragraph):
    answer = paragraph
    for s_index, w_index, word in paragraph.indexed_all_words():
        if isinstance(word, Verb):
            new_verb = word.to_basic_verb()
            if word.has_tags(WordTag.NEGATIVE):
                new_verb = new_verb.negative()
            answer = answer.set(s_index, w_index, new_verb)
    return answer
