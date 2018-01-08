# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

import os
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
styles = getSampleStyleSheet()


def create_pdf(save_folder, answer_texts, error_texts, error_font_size=13):
    file_prefix = get_file_prefix(save_folder)
    answer_filename = os.path.join(save_folder, file_prefix + 'answer.pdf')
    error_filename = os.path.join(save_folder, file_prefix + 'error.pdf')
    save_paragraphs_to_pdf(answer_filename, answer_texts, error_font_size - 1)
    save_paragraphs_to_pdf(error_filename, error_texts, error_font_size)


def get_file_prefix(folder):
    current = os.listdir(folder)
    current = [file_name for file_name in current if is_numbered_pdf(file_name)]
    if not current:
        next_num = 1
    else:
        current.sort()
        next_num = int(current[-1].split('_')[0]) + 1
    return '{:0>2}_'.format(next_num)


def is_numbered_pdf(filename: str):
    return filename[2] == '_' and filename[:2].isdigit() and filename.endswith('.pdf')


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
