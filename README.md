
[![Build Status](https://travis-ci.org/tingletech/greeker.py.png)](https://travis-ci.org/tingletech/greeker.py)

```
usage: greeker.py [-h] [--piglatin] [infile] [outfile]

Create greeked text for XML testing.

positional arguments:
  infile      input XML (or standard input)
  outfile     output greeked XML (or standard out)

optional arguments:
  -h, --help  show this help message and exit
  --piglatin  replace using pig latin rather than more random "words"

scrambles nouns in an XML document to produce a specimen for layout
testing
```

EXAMPLE
-------

test/sample3.xml

```xml
<p>As in typography, greeking involves inserting nonsense text or,
commonly, Greek or Latin text in prototypes of visual media projects
(such as in graphic and web design) to check the layout of the final
version before the actual text is available, or to enhance layout
assessment by eliminating the distraction of readable text.  Text
of this sort is known as "greeked text", "dummy text", or "jabberwocky
text".  Lorem ipsum is a commonly used example, though this is
derived from Latin, not Greek.</p><!-- http://en.wikipedia.org/wiki/Greeking -->
```

test/3klein.xml

```
<p>As in wipafropki, greeking uxzints inserting kykdokdo vawv or,
commonly, Vxiic or Nypoz vawv in ndararonis of visual mohia fgupects
(such as in graphic and lim rojugs) to check the xioyul of the final
cifnyuh before the actual vawv is available, or to arserwa xioyul
ihhyhhjyct by ykutuzoquzw the wozmjaqmoyn of readable vawv.  Vawv
of this meks is known as "greeked vawv", "pyllu vawv", or "jabberwocky
vawv".  Sutab uflin is a commonly used uxavqmu, though this is
derived from Nypoz, not Vxiic.</p><!-- http://en.wikipedia.org/wiki/Greeking -->
```

[I guess this is more like 1/2 greeking, since it is only the nouns]

INSTALL
-------

This command should install greeker.py and its dependencies.

Requires Python 2.6, or 2.7 -- does not work with Python 3 nor 2.5.

```sh
pip install https://github.com/tingletech/greeker.py/tarball/master
```

or if you haved checked out/downloaded this code, then you could go

```sh
pip install .
```

You will also need some data for the natural language toolkit to
function.  This command will grab the data for you.

```sh
python -m nltk.downloader punkt maxent_treebank_pos_tagger
```

or just install the nltk data

```sh
python -m nltk.downloader all
```

TODO
----

add "--attributes att1 att2 ..." command line option to specify xml 
attributes by local name that should be greeked. (default is no greeking of attributes)

set up unit tests using some sort of orthodox tool or method
