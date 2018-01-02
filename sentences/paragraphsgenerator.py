from sentences.backend.errormaker import ErrorMaker
from sentences.backend.grammarizer import Grammarizer
from sentences.backend.random_paragraph import RandomParagraph
from sentences.backend.wordconnector import convert_paragraph


class ParagraphsGenerator(object):
    def __init__(self, config_state):
        self._options = config_state.copy()
        self._paragraph_generator = None  # type: RandomParagraph
        self.create_paragraph_generator()

    def update_options(self, dictionary):
        self._options.update(dictionary)
        self.create_paragraph_generator()

    def _get_kwargs(self, *keys):
        return {key: self._options[key] for key in keys}

    def _get_present_tense_bool(self):
        return self._options['tense'] == 'simple_present'

    def create_paragraph_generator(self):
        kwargs = self._get_kwargs('probability_pronoun', 'countable_nouns', 'uncountable_nouns', 'verbs')
        self._paragraph_generator = RandomParagraph(**kwargs)

    def create_paragraph(self):
        paragraph_size = self._options['paragraph_size']
        if self._options['paragraph_type'] == 'pool':
            subj_pool = self._options['subject_pool']
            raw_paragraph = self._paragraph_generator.create_pool_paragraph(subj_pool, paragraph_size)
        else:
            raw_paragraph = self._paragraph_generator.create_chain_paragraph(paragraph_size)

        present_tense = self._get_present_tense_bool()
        kwargs = self._get_kwargs('probability_plural_noun', 'probability_negative_verb')
        grammarizer = Grammarizer(raw_paragraph, present_tense=present_tense, **kwargs)
        return grammarizer.generate_paragraph()

    def create_answer_and_error_texts(self):
        paragraph = self.create_paragraph()
        error_maker = ErrorMaker(paragraph, p_error=self._options['error_probability'],
                                 present_tense=self._get_present_tense_bool())
        error_methods = {
            'noun_errors': error_maker.create_noun_errors,
            'verb_errors': error_maker.create_verb_errors,
            'punctuation_errors': error_maker.create_period_errors
        }
        for key, method in error_methods.items():
            if self._options[key]:
                method()

        error_count = ' -- error count: {}'
        answer = convert_paragraph(error_maker.answer_paragraph) + error_count.format(error_maker.error_count)
        error = convert_paragraph(error_maker.error_paragraph)
        return answer, error

    def create_paragraphs(self):
        answers = []
        errors = []
        for _ in range(self._options['num_paragraphs']):
            answer, error = self.create_answer_and_error_texts()
            answers.append(answer)
            errors.append(error)
        return answers, errors
