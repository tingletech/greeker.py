""" greeker.py 
    pig-latinizes an XML document to produce a specimine for layout testing
"""
import sys
import nltk
from lxml import etree
import re
import inflect
p = inflect.engine()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    # TODO: make this real the argv
    greekize_file("sample.xml", "out.xml")

def greekize_file(infile, outfile):
    """greekize the infile to outfile"""
    file = etree.parse(infile)
    text_nodes = file.xpath("//text()")
    # pull sample text from the text nodes
    text = ''.join(text_nodes)
    greek_text = greekize_text(text).split()
    # pass an array because we are recursivly .pop(0) the new words from it
    update_xml(file.getroot(), greek_text)
    file.write(outfile, pretty_print=True)

def greekize_text(text):
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
                piglatin = p.plural_noun(pig_latinize(singular))
                text = re.sub(tagged_word[0]+"(\W)",piglatin+"\\1",text)
            # replace proper nouns and nouns
            if tagged_word[1] in ['NN', 'NNP']:
                text = re.sub(tagged_word[0]+"(\W)",pig_latinize(tagged_word[0])+"\\1",text)
    return text

def update_xml(node, greek_text):
    """update the xml document with the new words"""
    new_text = ''
    # TODO; construction of the new_ texts need to retain whitespace
    # pop some new words off the greek_text array
    if node.text:
        for word in node.text.split():
            new_text += greek_text.pop(0)
            new_text += " "
        # set the new text, up to the first child element
        node.text = new_text
    # this gets child elements... not all DOM nodes	
    for desc in node.getchildren():
        # recursive call
        update_xml(desc, greek_text)
    # ElementTree supports mixed content via .tail... 
    new_mixed_text = ''
    if node.tail:
        for word in node.tail.split():
            new_mixed_text += greek_text.pop(0)
            new_mixed_text += " "
        node.tail = new_mixed_text

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
