from sentences.words.punctuation import Punctuation


def connect_words(word_list):
    answer = ''
    for word in word_list:
        if isinstance(word, Punctuation):
            answer = answer.rstrip()
        answer += word.value + ' '
    return answer.rstrip()
