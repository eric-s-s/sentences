# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

import os
from datetime import datetime
import re

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
styles = getSampleStyleSheet()


def create_pdf(save_folder, answer_texts, error_texts, error_font_size=13, named_prefix=''):
    file_prefix = get_file_prefix(save_folder, named_prefix)
    answer_filename = os.path.join(save_folder, file_prefix + 'answer.pdf')
    error_filename = os.path.join(save_folder, file_prefix + 'error.pdf')
    save_paragraphs_to_pdf(answer_filename, answer_texts, error_font_size - 1)
    save_paragraphs_to_pdf(error_filename, error_texts, error_font_size)


def get_file_prefix(folder, named_prefix=''):
    current = os.listdir(folder)
    group = [file_name for file_name in current if is_numbered_member_of_prefix_group(file_name, named_prefix)]
    if not group:
        next_num = 1
    else:
        group.sort()
        slice_at = len(named_prefix)
        next_num = int(group[-1][slice_at: slice_at + 2]) + 1
    return '{}{:0>2}_'.format(named_prefix, next_num)


def is_numbered_member_of_prefix_group(filename: str, prefix):
    return filename.startswith(prefix) and re.match('{}\d\d_'.format(prefix), filename) is not None


def save_paragraphs_to_pdf(file_name, paragraphs, font_size):
    head_foot = 1.0*cm
    margin = 1.3*cm

    title = os.path.split(file_name)[1]

    doc = SimpleDocTemplate(file_name, pagesize=A4, rightMargin=margin, leftMargin=margin,
                            bottomMargin=head_foot, topMargin=head_foot, title=title)
    Story = [Spacer(0.5, 0.5 * cm)]
    style = styles["Normal"]
    style.fontSize = font_size
    style.leading = style.fontSize * 2.5

    for paragraph in paragraphs:
        text = paragraph.replace('<bold>', '<b><u>')
        text = text.replace('</bold>', '</u></b>')

        p = Paragraph(text, style)
        Story.append(p)
        Story.append(Spacer(0.5, 0.5 * cm))
    doc.build(Story, onFirstPage=insert_footer, onLaterPages=insert_footer)


def insert_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "{} : page {}, {}".format(doc.title,
                                                               doc.page,
                                                               datetime.now().strftime('%Y/%m/%d-%H:%M')))
    canvas.restoreState()
