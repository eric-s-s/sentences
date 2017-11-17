import sentences.wordconnector as wc
import sentences.random_paragraph as para
import sentences.grammarizer as grammar
import sentences.errormaker as error


if __name__ == '__main__':

    paragraph_maker = para.RandomParagraph()
    correct_p = []
    error_p = []
    for _ in range(4):
        answer = paragraph_maker.create_chain_paragraph(15)
        paragraph = grammar.Grammarizer(answer).generate_paragraph()
        e_maker = error.ErrorMaker(paragraph, p_error=0.2)
        e_maker.create_all_errors()
        correct_p.append(wc.convert_paragraph(e_maker.answer_paragraph))
        error_p.append(wc.convert_paragraph(e_maker.error_paragraph))

    with open('correct.txt', 'w') as f:
        f.write('\n\n'.join(correct_p))

    with open('mistake.txt', 'w') as f:
        f.write('\n\n'.join(error_p))
