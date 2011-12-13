#!/usr/bin/env python
""" greeker.py 
    scrambles nouns in an XML document to produce a specimine for layout testing
"""
import sys
import argparse
import nltk
from lxml import etree
import re
import inflect
p = inflect.engine()
import random
from string import maketrans
import argparse

def main(argv=None):

    parser = argparse.ArgumentParser(description='Create greeked text for XML testing.',
                     epilog="scrambles nouns in an XML document to produce a specimine for layout testing")

    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                     help='input XML (or standard input)',
                     default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                     help='output greeked XML (or standard out)',
                     default=sys.stdout)
    parser.add_argument('--piglatin', action='store_const',
                   const='pig',
                   help='replace using pig latin rather than more random "words"')

    if argv is None:
        argv = parser.parse_args()

    if argv.piglatin:
        scrambler = pig_latinize
    else:
        scrambler = consonant_vowel_sensitive_random_word

    greekize_file(argv.infile, argv.outfile, scrambler)

def greekize_file(infile, outfile, scrambler):
    """greekize the infile to outfile"""
    file = etree.parse(infile)
    text_nodes = file.xpath("//text()")
    # pull sample text from the text nodes
    text = ''.join(text_nodes)
    greek_text = greekize_text(text, scrambler).split()
    # pass an array because we are recursivly .pop(0) the new words from it
    update_xml(file.getroot(), greek_text)
    file.write(outfile, pretty_print=True)

def greekize_text(text, scrambler):
    """takes a string of text as input; changes nouns to pig latin"""

    # array of all the sentences (is this necessary?)
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    # part of speech tagging 
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

    # pig latinize all nouns in the text
    for sentence in tagged_sentences:
        for tagged_word in sentence:
            # skip "(", not sure what other characters nltk will put in the parse tree
            if tagged_word[0] in ["(", ")", "[", "]"]:
                continue
            # replace plural nouns with pig latin
            if tagged_word[1] == 'NNS':
                singular = p.singular_noun(tagged_word[0]);
                scrambled = p.plural_noun(scrambler(singular))
                text = re.sub(tagged_word[0]+"(\W)",scrambled+"\\1",text)
            # replace proper nouns and nouns
            if tagged_word[1] in ['NN', 'NNP']:
                text = re.sub(tagged_word[0]+"(\W)",scrambler(tagged_word[0])+"\\1",text)
    return text

def update_xml(node, greek_text):
    """update the xml document with the new words"""
    # TODO; construction of the new_ texts need to retain whitespace
    # pop some new words off the greek_text array
    if node.text:
        node.text = update_text(node.text, greek_text)
    # this gets child elements... not all DOM nodes	
    for desc in node.getchildren():
        # recursive call
        update_xml(desc, greek_text)
    # ElementTree supports mixed content via .tail... 
    if node.tail:
        node.tail = update_text(node.tail, greek_text)

def update_text(text_from_node,greek_text):
    """create new string for element .text or .tail"""
    # if I don't have any words; just copy the whitespace
    if not(re.search("\w", text_from_node)):
        return text_from_node
    # otherwise; pop some words off the stack
    new_text = ''
    for word in text_from_node.split():
        new_text += greek_text.pop(0)
        new_text += " "
    return new_text

def consonant_vowel_sensitive_random_word(word):
    """scramble word, keeping vowles in the same place"""
    # based on klein method here: https://gist.github.com/1468557
    # specifically here https://gist.github.com/1468557/c3d1ebf5f9ae2805abf9fc242c1a3839dead6843
    # seed the random generator with the word, so it will be less random
    random.seed(word)
    vowles = "aeiouy"
    consonants = "bcdfghjklmnpqrstvwxz"
    new_vowles = list(vowles)
    new_consonants = list(consonants)
    # shuffles in place
    random.shuffle(new_vowles)
    random.shuffle(new_consonants)
    vowles = vowles + vowles.upper()
    consonants = consonants + consonants.upper()
    trans_to = ''.join(new_vowles) + ''.join(new_vowles).upper()
    trans_to += ''.join(new_consonants) + ''.join(new_consonants).upper()
    randomize = maketrans(vowles + consonants, trans_to)
    return word.translate(randomize)

def pig_latinize(noun):
    """ convert one word into pig latin """ 
    # http://pythonicprose.blogspot.com/2009/09/python-pig-latin-generator.html
    word = noun.lower()
    m = len(word)
    vowels = "a", "e", "i", "o", "u", "y" 
    # short words are not converted 
    if m<3 or word=="the":
        return word
    else:
        # m==0 when the word starts with a vowel
        for i in vowels:
            if word.find(i) < m and word.find(i) != -1:
                m = word.find(i)
        if m==0:
            piglatin = word+"way" 
        else:
            piglatin = word[m:]+word[:m]+"ay"
        # give the return the same title case as the input
        if noun.istitle():
            piglatin = piglatin.lower().title()
        return piglatin

# main() idiom for importing into REPL for debugging 
if __name__ == "__main__":
    sys.exit(main())
