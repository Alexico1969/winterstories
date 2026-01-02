import nltk
import statistics
from nltk.tokenize import sent_tokenize, word_tokenize

text = open("sample.txt").read()

sentences = sent_tokenize(text)
sentence_lengths = [len(word_tokenize(s)) for s in sentences]

print("Avg sentence length:", statistics.mean(sentence_lengths))
print("Sentence length variance:", statistics.pvariance(sentence_lengths))
