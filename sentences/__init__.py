import os

APP_NAME = 'sentence_mangler'

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
DEFAULT_CONFIG = os.path.join(DATA_PATH, 'default.cfg')

COUNTABLE_NOUNS_CSV = 'nouns.csv'
UNCOUNTABLE_NOUNS_CSV = 'uncountable.csv'
VERBS_CSV = 'verbs.csv'


