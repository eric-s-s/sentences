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
Title = "Hello world"
pageinfo = "platypus example"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "Page %d %s" % (doc.page, doc.filename))
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "Page %d %s" % (doc.page, doc.filename))
    canvas.restoreState()


def go(file_name, paragraphs):
    head_foot = 1.0*cm
    margin = 1.3*cm
    doc = SimpleDocTemplate(file_name, pagesize=A4, rightMargin=margin, leftMargin=margin,
                            bottomMargin=head_foot, topMargin=head_foot)
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
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


def get_file_suffix():
    current = os.listdir('./pdfs')
    if not current:
        return '_0.pdf'
    nums = [get_num(file_name) for file_name in current]
    return '_{}.pdf'.format(max(nums) + 1)


def get_num(pdf_filename):
    minus_pdf = pdf_filename[:-len('.pdf')]
    els = minus_pdf.split('_')
    return int(els[-1])


if __name__ == "__main__":
    present, past = generate_text()
    suffix = get_file_suffix()
    answer = './pdfs/answer' + suffix
    error = './pdfs/error' + suffix
    go(answer, present[0])
    go(error, present[1])
