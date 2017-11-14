import sentences.raw_word_randomisation as sg
import sentences.wordconnector as wc
import sentences.raw_paragraph_randomisation as para

gener = sg.RawWordsRandomisation()

# for _ in range(10):
#     print(wc.connect_words(gener.sentence()))

paragrapher = para.RawParagraphRandomisation()

# answer = paragrapher.create_pool_paragraph(3, 10)
#
# for sentence in answer:
#     print(wc.connect_words(sentence))
#
# print()

answer = paragrapher.create_chain_paragraph(15)
# for sentence in answer:
#     print(wc.connect_words(sentence))

import itertools



def line_print(big_str):
    line_len = 65
    print_list = []
    while big_str:
        line = big_str[:line_len]
        if len(line) < line_len:
            pass
        else:
            index = line.rfind(' ')
            line = line[:index]
        big_str = big_str[len(line) + 1:]
        print_list.append(line)
    print('\n'.join(print_list))


import sentences.grammarizer as grammar
import sentences.errormaker as error
print()
paragraph = grammar.Grammarizer(answer).generate_paragraph()
line_print(wc.convert_paragraph(paragraph))
print()
e = error.ErrorMaker(paragraph, p_error=0.2)
e.create_all_errors()
line_print(wc.convert_paragraph(e.error_paragraph))
print()

correct_p = []
error_p = []
for _ in range(5):
    answer = paragrapher.create_chain_paragraph(15)
    paragraph = grammar.Grammarizer(answer).generate_paragraph()
    e_maker = error.ErrorMaker(paragraph, p_error=0.2)
    e_maker.create_all_errors()
    correct_p.append(wc.convert_paragraph(e_maker.answer_paragraph))
    error_p.append(wc.convert_paragraph(e_maker.error_paragraph))

with open('correct.txt', 'w') as f:
    f.write('\n\n'.join(correct_p))

with open('mistake.txt', 'w') as f:
    f.write('\n\n'.join(error_p))
