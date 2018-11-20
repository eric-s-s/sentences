from sentences.alt_backend.new_grammarizer import NewGrammarizer
from sentences.backend.random_assignments.plurals_assignement import get_countable_nouns, PluralsAssignment
from sentences.tags.status_tag import StatusTag


def create_answer_str(paragraph_str, base_paragraph):
    new_base = _get_plurals_paragraph(base_paragraph, paragraph_str)
    grammarizer = NewGrammarizer(new_base)
    if base_paragraph.tags.has(StatusTag.SIMPLE_PAST):
        answer = grammarizer.grammarize_to_past_tense()
    else:
        answer = grammarizer.grammarize_to_present_tense()
    return str(answer)


def _get_plurals_paragraph(base_paragraph, paragraph_str):
    countable_nouns = get_countable_nouns(base_paragraph)
    plurals = [noun for noun in countable_nouns if noun.plural().value in paragraph_str]
    new_base = PluralsAssignment(base_paragraph).assign_plural(plurals)
    return new_base

