# https://gist.github.com/322906/
import nltk
import nltk.data
import re
import inflect
p = inflect.engine()

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
            piglatin = word+"way" 
        else:
            piglatin = word[m:]+word[:m]+"ay"
        # keep the word in title case
        if word.istitle():
            piglatin = piglatin.lower().title()
        return piglatin

# open sample input
global sample
with open('sample-long.txt', 'r') as f:
    sample = f.read()

sentences = nltk.sent_tokenize(sample)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

for sentence in tagged_sentences:
    for tagged_word in sentence:
        print tagged_word
        # skip "("
        if tagged_word[0] in ["(", ")"]:
            continue
        # replace plural nouns with pig latin
        if tagged_word[1] == 'NNS':
            singular = p.singular_noun(tagged_word[0]);
            piglatin = p.plural_noun(makePigLatin(singular))
            sample = re.sub(tagged_word[0]+"(\W)",piglatin+"\\1",sample)
        # replace proper nouns and nouns
        if tagged_word[1] in ['NN', 'NNP']:
            sample = re.sub(tagged_word[0]+"(\W)",makePigLatin(tagged_word[0])+"\\1",sample)

print sample