# https://gist.github.com/322906/
import nltk
import nltk.data
import re

# http://pythonicprose.blogspot.com/2009/09/python-pig-latin-generator.html
def makePigLatin(word):
    """ convert one word into pig latin """ 
    m  = len(word)
    vowels = "a", "e", "i", "o", "u", "y" 
    # short words are not converted 
    if m<3 or word=="the":
        return word
    else:
        for i in vowels:
            if word.find(i) < m and word.find(i) != -1:
                m = word.find(i)
        if m==0:
            return word+"way" 
        else:
            return word[m:]+word[:m]+"ay" 

# open sample input
global sample
with open('sample.txt', 'r') as f:
    sample = f.read()

sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

for sentence in tagged_sentences:
    for tagged_word in sentence:
        print tagged_word
        if tagged_word[1] == 'NNP':
            sample = re.sub(tagged_word[0],makePigLatin(tagged_word[0]).lower().title(),sample)
        if tagged_word[1] == 'NN':
            if tagged_word[0].istitle():
                sample = re.sub(tagged_word[0],makePigLatin(tagged_word[0]).lower().title(),sample)
            else:
                sample = re.sub(tagged_word[0],makePigLatin(tagged_word[0]),sample)

print sample