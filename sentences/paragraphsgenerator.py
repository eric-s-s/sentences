from sentences.backend.errormaker import ErrorMaker
from sentences.backend.grammarizer import Grammarizer
from sentences.backend.random_paragraph import RandomParagraph
from sentences.backend.wordconnector import convert_paragraph
from sentences.backend.loader import verbs, uncountable_nouns, countable_nouns, proper_nouns


class ParagraphsGenerator(object):
    def __init__(self, config_state):
        """

        :config_state required keys:
        - 'countable_nouns'
        - 'uncountable_nouns'
        - 'proper_nouns'
        - 'verbs'

        - 'error_probability'
        - 'noun_errors'
        - 'pronoun_errors'
        - 'verb_errors'
        - 'is_do_errors'
        - 'preposition_transpose_errors'
        - 'punctuation_errors'


        - 'tense'
        - 'probability_plural_noun'
        - 'probability_negative_verb'
        - 'probability_pronoun'

        - 'paragraph_type'
        - 'subject_pool'
        - 'num_paragraphs'
        - 'paragraph_size'
        """
        self._options = {}
        self._verbs_list = []
        self._nouns_list = []
        self.update_options(config_state)

    def load_lists_from_file(self):
        self._verbs_list = verbs(self._options['verbs'])

        self._nouns_list = countable_nouns(self._options['countable_nouns'])
        self._nouns_list += uncountable_nouns(self._options['uncountable_nouns'])
        self._nouns_list += proper_nouns(self._options['proper_nouns'])

    def update_options(self, dictionary):
        reload_lists = self._is_reload_required(dictionary)
        self._options.update(dictionary)
        if reload_lists:
            self.load_lists_from_file()

    def _is_reload_required(self, dictionary):
        all_word_lists = (self._verbs_list, self._nouns_list)
        if any(word_list == [] for word_list in all_word_lists):
            return True

        file_keys = [key for key in ('verbs', 'countable_nouns', 'uncountable_nouns', 'proper_nouns')
                     if key in dictionary]
        if not file_keys:
            return False
        return any(dictionary[key] != self._options[key] for key in file_keys)

    def create_paragraph(self):
        paragraph_generator = self._create_paragraph_generator()
        paragraph_size = self._options['paragraph_size']
        if self._options['paragraph_type'] == 'pool':
            subj_pool = self._options['subject_pool']
            raw_paragraph = paragraph_generator.create_pool_paragraph(subj_pool, paragraph_size)
        else:
            raw_paragraph = paragraph_generator.create_chain_paragraph(paragraph_size)

        present_tense = self._get_present_tense_bool()
        kwargs = self._get_kwargs('probability_plural_noun', 'probability_negative_verb')
        grammarizer = Grammarizer(raw_paragraph, present_tense=present_tense, **kwargs)
        return grammarizer.generate_paragraph()

    def _create_paragraph_generator(self):
        probability_pronoun = self._options['probability_pronoun']
        return RandomParagraph(probability_pronoun, self._verbs_list, self._nouns_list)

    def _get_present_tense_bool(self):
        return self._options['tense'] == 'simple_present'

    def _get_kwargs(self, *keys):
        return {key: self._options[key] for key in keys}

    def create_answer_and_error_texts(self):
        paragraph = self.create_paragraph()
        error_maker = ErrorMaker(paragraph, p_error=self._options['error_probability'])

        options_keys = {
            error_maker.create_noun_errors: 'noun_errors',
            error_maker.create_pronoun_errors: 'pronoun_errors',
            error_maker.create_verb_errors: 'verb_errors',
            error_maker.create_is_do_errors: 'is_do_errors',
            error_maker.create_preposition_transpose_errors: 'preposition_transpose_errors',
            error_maker.create_period_errors: 'punctuation_errors',
        }
        for method in error_maker.method_order:
            if self._options[options_keys[method]]:
                method()

        error_count = ' -- error count: {}'
        answer = convert_paragraph(error_maker.answer_paragraph) + error_count.format(error_maker.error_count)
        error = convert_paragraph(error_maker.error_paragraph)
        return answer, error

    def create_answer_and_error_paragraphs(self):
        answers = []
        errors = []
        for _ in range(self._options['num_paragraphs']):
            answer, error = self.create_answer_and_error_texts()
            answers.append(answer)
            errors.append(error)
        return answers, errors
