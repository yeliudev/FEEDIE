import nltk

sentence = """Jarvis would you please bring me a piece of bread"""
words = nltk.word_tokenize(sentence)
print(words)

tagged = nltk.pos_tag(words)
print(tagged)
