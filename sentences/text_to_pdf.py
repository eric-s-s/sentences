# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

import os

from sentences.generate_text import generate_text

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
styles = getSampleStyleSheet()


def insert_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "{} : page {}".format(doc.title, doc.page))
    canvas.restoreState()


def create_pdf(location, file_name, paragraphs):
    head_foot = 1.0*cm
    margin = 1.3*cm
    if '\\' in location:
        sep = '\\'
    else:
        sep = '/'
    full_filename = '{}{}{}'.format(location, sep, file_name)

    doc = SimpleDocTemplate(full_filename, pagesize=A4, rightMargin=margin, leftMargin=margin,
                            bottomMargin=head_foot, topMargin=head_foot, title=file_name)
    Story = [Spacer(0.5, 0.5 * cm)]
    style = styles["Normal"]
    style.fontSize = 13
    style.leading = style.fontSize * 2.5

    for paragraph in paragraphs:
        text = paragraph.replace('<bold>', '<b><u>')
        text = text.replace('</bold>', '</u></b>')

        p = Paragraph(text, style)
        Story.append(p)
        Story.append(Spacer(0.5, 0.5 * cm))
    doc.build(Story, onFirstPage=insert_footer, onLaterPages=insert_footer)


def get_file_prefix():
    current = os.listdir('./pdfs')
    if not current:
        return '01_'
    current.sort()
    next_num = int(current[-1].split('_')[0]) + 1
    if next_num < 10:
        return '0{}_'.format(next_num)
    return '{}_'.format(next_num)


if __name__ == "__main__":
    present, past = generate_text()
    prefix = get_file_prefix()
    folder = './pdfs'
    answer = prefix + 'answer.pdf'
    error = prefix + 'error.pdf'
    create_pdf(folder, answer, present[0])
    create_pdf(folder, error, present[1])

    # past_answer = prefix + 'past_answer.pdf'
    # past_error = prefix + 'past_error.pdf'
    # create_pdf(folder, past_answer, past[0])
    # create_pdf(folder, past_error, past[1])
