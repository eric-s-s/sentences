from sentences.random_paragraph import RandomParagraph
from sentences.wordconnector import convert_paragraph
from sentences.grammarizer import Grammarizer
from sentences.errormaker import ErrorMaker

if __name__ == '__main__':

    paragraph_maker = RandomParagraph()
    correct_p = []
    error_p = []
    for _ in range(4):
        answer = paragraph_maker.create_chain_paragraph(15)
        paragraph = Grammarizer(answer).generate_paragraph()
        e_maker = ErrorMaker(paragraph, p_error=0.2)
        e_maker.create_all_errors()
        correct_p.append(convert_paragraph(e_maker.answer_paragraph))
        error_p.append(convert_paragraph(e_maker.error_paragraph))

    with open('correct.txt', 'w') as f:
        f.write('\n\n'.join(correct_p))

    with open('mistake.txt', 'w') as f:
        f.write('\n\n'.join(error_p))
