import tkinter as tk
from tkinter.font import nametofont
import os

from sentences import DATA_PATH


def get_read_me_paragraphs():
    with open(os.path.join(DATA_PATH, 'README.txt'), 'r') as f:
        paragraphs = group_text(f.read().split('\n'))
    return paragraphs


def group_text(text_lines):
    answer = []
    paragraph = [text_lines[0]]
    for line in text_lines[1:]:
        if is_new_paragraph(line):
            if not paragraph[0]:
                del paragraph[0]
            answer.append(' '.join(paragraph))
            paragraph = [line.rstrip()]
        else:
            paragraph.append(line.strip())
    answer.append(' '.join(paragraph))
    return answer


def is_new_paragraph(line):
    if not line or line.strip().startswith('-') or line.strip().startswith('='):
        return True
    return False


def find_second_margin(paragraph):
    index = paragraph.find(':')
    if index == -1:
        return 0
    return index + 2


class ReadMeText(tk.Text):
    def __init__(self, *args, **kwargs):
        super(ReadMeText, self).__init__(*args, **kwargs)

        font_size = nametofont(self.cget('font')).cget('size')

        paragraphs = get_read_me_paragraphs()
        for index, paragraph in enumerate(paragraphs):
            style = str(index)
            second_margin = find_second_margin(paragraph) * font_size
            self.tag_config(style, lmargin1=0, lmargin2=second_margin)
            self.insert(tk.END, paragraph + '\n\n', style)
        self.config(state=tk.DISABLED)
