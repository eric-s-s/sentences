import re
import os
from sentences import DATA_PATH


def upper_repl(match):
    return match.group(1).upper()


def double_star_to_upper(readme):
    matcher = r'\*\*([^*]+)\*\*'
    return re.sub(matcher, upper_repl, readme)


def single_star_to_quotes(readme):
    matcher = r'(?<!\*)\*([^*]+)\*(?!\*)'
    return re.sub(matcher, r'"\1"', readme)


def replace_stars(readme):
    return single_star_to_quotes(double_star_to_upper(readme))


def repl_intro(match):
    intro_text = ("\n\nThis app creates randomly generated paragraphs and then assigns specific\n" +
                  "kinds of errors to those paragraphs. It outputs this text to a pdf file.\n\n")
    return match.group(1) + intro_text


def replace_intro(text):
    readme_start = r"(sentences v\d+\.\d+\s+==============).+(?=GUI options details:)"
    return re.sub(readme_start, repl_intro, text, flags=re.DOTALL)


def re_format_readme():
    with open(os.path.join(os.path.dirname(os.path.dirname(DATA_PATH)), 'README.rst'), 'r') as f:
        old_text = f.read()

    with open(os.path.join(DATA_PATH, 'README.txt'), 'w') as f:
        f.write(replace_intro(replace_stars(old_text)))


if __name__ == '__main__':
    re_format_readme()
