# Sample platypus document
# From the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1

import os
from datetime import datetime

from sentences.generate_text_delete_me import generate_text

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]
styles = getSampleStyleSheet()


def get_target_dir():
    documents_path = get_documents_folder()
    app_folder = os.path.join(documents_path, 'sentence_mangler')
    folder = os.path.join(app_folder, 'pdfs')
    if not os.path.exists(app_folder):
        os.mkdir(app_folder)
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


def get_documents_folder():
    user_location = os.path.expanduser('~')
    user_folder = os.listdir(user_location)
    if 'My Documents' in user_folder:
        return os.path.join(user_location, 'My Documents')
    elif 'Documents' in user_folder:
        return os.path.join(user_location, 'Documents')
    else:
        return user_location


def insert_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(cm, 0.75 * cm, "{} : page {}, {}".format(doc.title,
                                                               doc.page,
                                                               datetime.now().strftime('%Y/%m/%d-%H:%M')))
    canvas.restoreState()


def create_pdf(location, file_name, paragraphs):
    head_foot = 1.0*cm
    margin = 1.3*cm

    full_filename = os.path.join(location, file_name)

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


def get_file_prefix(folder):
    current = os.listdir(folder)
    current = [file_name for file_name in current if '_' in file_name and file_name[0].isdigit()]
    if not current:
        return '01_'
    current.sort()
    next_num = int(current[-1].split('_')[0]) + 1
    if next_num < 10:
        return '0{}_'.format(next_num)
    return '{}_'.format(next_num)


def main():

    present, past = generate_text()
    folder = get_target_dir()

    prefix = get_file_prefix(folder)

    answer = prefix + 'answer.pdf'
    error = prefix + 'error.pdf'
    create_pdf(folder, answer, present[0])
    create_pdf(folder, error, present[1])


if __name__ == "__main__":
    main()

    # past_answer = prefix + 'past_answer.pdf'
    # past_error = prefix + 'past_error.pdf'
    # save_paragraphs_to_pdf(folder, past_answer, past[0])
    # save_paragraphs_to_pdf(folder, past_error, past[1])
