import sentences.raw_word_randomisation as sg
import sentences.wordconnector as wc
import sentences.raw_paragraph_randomisation as para

gener = sg.RawWordsRandomisation()

# for _ in range(10):
#     print(wc.connect_words(gener.sentence()))

paragrapher = para.RawParagraphRandomisation()

answer = paragrapher.create_pool_paragraph(3, 10)

for sentence in answer:
    print(wc.connect_words(sentence))

print()

answer = paragrapher.create_chain_paragraph(10)
for sentence in answer:
    print(wc.connect_words(sentence))

import itertools

print(wc.connect_words(itertools.chain.from_iterable(answer)))
