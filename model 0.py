import nltk

while True:
    sentence = input("Sentence: ")
    print(nltk.pos_tag(nltk.word_tokenize(sentence)))
