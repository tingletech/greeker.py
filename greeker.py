#!/usr/bin/env python
""" greeker.py 
    scrambles nouns in an XML document to produce a specimen for layout testing
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
from difflib import SequenceMatcher

def main(argv=None):
    # argument parser 
    parser = argparse.ArgumentParser(
                     description='Create greeked text for XML testing.',
                     epilog="scrambles nouns in an XML document to produce \
                             a specimen for layout testing")
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

    # pick the text transformation method
    if argv.piglatin:
        scrambler = pig_latinize
    else:
        scrambler = consonant_vowel_sensitive_random_word

    # call the function that does the work
    greekize_file(argv.infile, argv.outfile, scrambler)

def greekize_file(infile, outfile, scrambler):
    """greekize the infile to outfile"""
    file = etree.parse(infile)
    text_nodes = file.xpath("//text()")
    # pull sample text from the text nodes
    text = ''.join(text_nodes)
    greek_text = greekize_text(text, scrambler)
    # pass an array because we are recursivly .pop(0) the new words from it
    update_xml(file.getroot(), greek_text.split())
    file.write(outfile)

def greekize_text(text, scrambler):
    """takes a string of text as input; changes nouns to pig latin"""

    # array of all the sentences (is this necessary?)
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    # part of speech tagging 
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]

    # scramble all nouns in the text
    for sentence in tagged_sentences:
        for tagged_word in sentence:
            # print tagged_word
            # skip "(", not sure what other characters nltk will put in the parse tree
            #if tagged_word[0] in ["(", ")", "[", "]"]: XXX
            if re.search("^\W+$", tagged_word[0]):
                continue

            # replace plural nouns with pig latin
            if tagged_word[1] == 'NNS':
                # .singular_noun can return a boolean False or a string
                singular = p.singular_noun(tagged_word[0]);
                if singular:
                    scrambled = p.plural_noun(scrambler(singular))
                else:
                    scrambled = scrambler(tagged_word[0])
                text = re.sub(tagged_word[0]+"(\W)",scrambled+"\\1",text)

            # replace proper nouns and nouns
            if tagged_word[1] in ['NN', 'NNP']:
                text = re.sub(tagged_word[0]+"(\W)",scrambler(tagged_word[0])+"\\1",text)
    return text

def update_xml(node, greek_text):
    """update the xml document with the new words"""

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

def update_text(text_from_node, greek_text):
    """create new string for element .text or .tail"""

    #print "text_from_node"
    #print text_from_node.split()
    #print "greek_text"
    #print greek_text

    # if I don't have any words; just copy the whitespace
    #if not(re.search("\w", text_from_node)):
    if text_from_node.isspace() or text_from_node=='':
        return text_from_node

    # otherwise; pop some words off the stack
    new_text = ''
    # http://stackoverflow.com/questions/647655/python-regex-split-and-special-character
    for word in re.compile("(\s)").split(text_from_node):
        # copy whitespace 
        if (word.isspace() or word ==''):
            new_text += word
        # pop the word off the stack
        else:
            new_text += smart_pop(word, greek_text)
    return new_text

def smart_pop(word, greek_text):
    """messy logic to deal with mixed content with no spaces"""
    # if we run out of words, just keep going...
    if len(greek_text) == 0:
        return "ERROR"
    pop_off = greek_text.pop(0)
    # word off the stack ends in a non-word character that word does not end in
    if re.search("\W$", pop_off) and pop_off[-1] != word[-1]:
        overlap = SequenceMatcher(lambda x: re.search("\w",x), 
                                  word, 
                                  pop_off)
        # no overlapping non-word pards
        if len(overlap.get_matching_blocks()) - 1 == 0:
            # put the non-word back on the stack; return only the wordchars out
            front, back = re.search("(\w+)(\W.*)$",pop_off).group(1, 2)
            greek_text.insert(0,back)
            return front
        
        # overlapping non-word parts
        else:
            # point at which the overlap starts ([0]) in pop_off ([1])
            point = overlap.get_matching_blocks()[0][1]
            # put the back of the word back on the stack
            greek_text.insert(0,pop_off[point+1:len(pop_off)])
            # return the start
            return pop_off[0:point+1]
    # things that start with a non-word in pop_off and have different word pattern
    elif re.search("^\W+\w.*$", pop_off) and not(re.search("^\W+\w.*$", word)):
            front, back = re.search("(\W+)(\w.*)$",pop_off).group(1, 2)
            greek_text.insert(0,back)
            return front
        
    return pop_off

def consonant_vowel_sensitive_random_word(word):
    """scramble word, keeping vowles in the same place"""
    # based on klein method here: https://gist.github.com/1468557
    # specifically here https://gist.github.com/1468557/c3d1ebf5f9ae2805abf9fc242c1a3839dead6843
    # add an exception for these ^[Aa]|[Aa]n|[Tt]he$
    # seed the random generator with the word, so it will be less random
    #if re.search('^[Aa]|[Aa]n|[Tt]he$', word):
    #   return word
    random.seed(word)
    vowles = u"aeiouy"
    consonants = u"bcdfghjklmnpqrstvwxz"
    new_vowles = list(vowles)
    new_consonants = list(consonants)
    # shuffles in place
    random.shuffle(new_vowles)
    random.shuffle(new_consonants)
    vowles = vowles + vowles.upper()
    consonants = consonants + consonants.upper()
    letters = vowles + consonants
    trans_to = ''.join(new_vowles) + ''.join(new_vowles).upper()

    trans_to += ''.join(new_consonants) + ''.join(new_consonants).upper()
    # http://stackoverflow.com/questions/1324067/how-do-i-get-str-translate-to-work-with-unicode-strings
    randomize = maketrans(vowles + consonants, trans_to)
    return word.encode("utf-8").translate(randomize)

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
