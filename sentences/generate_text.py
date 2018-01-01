from sentences.backend.errormaker import ErrorMaker
from sentences.backend.grammarizer import Grammarizer
from sentences.backend.random_paragraph import RandomParagraph
from sentences.backend.wordconnector import convert_paragraph


def generate_text(num_paragraphs=4, paragraph_size=15, subject_pool=0,
                  p_pronoun=0.2, p_plural=0.3, p_negative=0.3,
                  p_error=0.2,
                  noun_errors=True, verb_errors=True, period_errors=True,
                  verb_file='', countable_file='', uncountable_file=''):

    raw_paragraph_maker = RandomParagraph(p_pronoun=p_pronoun, verb_file=verb_file,
                                          countable_file=countable_file, uncountable_file=uncountable_file)
    present_answers = []
    present_errors = []
    past_answers = []
    past_errors = []
    for _ in range(num_paragraphs):
        if subject_pool:
            raw_paragraph = raw_paragraph_maker.create_pool_paragraph(subject_pool, paragraph_size)
        else:
            raw_paragraph = raw_paragraph_maker.create_chain_paragraph(paragraph_size)

        grammarizer = Grammarizer(raw_paragraph, p_plural=p_plural, p_negative=p_negative, present_tense=True)
        present_tense = grammarizer.generate_paragraph()
        grammarizer.present_tense = False
        past_tense = grammarizer.generate_paragraph()

        for_present = ErrorMaker(present_tense, present_tense=True, p_error=p_error)
        for_past = ErrorMaker(past_tense, present_tense=False, p_error=p_error)

        if noun_errors:
            for_present.create_noun_errors()
            for_past.create_noun_errors()
        if verb_errors:
            for_present.create_verb_errors()
            for_past.create_verb_errors()
        if period_errors:
            for_present.create_period_errors()
            for_past.create_period_errors()

        error_count = ' -- error count: {}'
        present_answer = convert_paragraph(for_present.answer_paragraph) + error_count.format(for_present.error_count)
        past_answer = convert_paragraph(for_past.answer_paragraph) + error_count.format(for_past.error_count)

        present_answers.append(present_answer)
        present_errors.append(convert_paragraph(for_present.error_paragraph))
        past_answers.append(past_answer)
        past_errors.append(convert_paragraph(for_past.error_paragraph))

    return (present_answers, present_errors), (past_answers, past_errors)
