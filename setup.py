from distutils.core import setup
setup(name='greeker',
      version='0.3-git',
      description="scrambles nouns in an XML document to produce a specimen for layout testing",
      author="Brian Tingle",
      author_email="brian.tingle.cdlib.org@gmail.com",
      url="http://tingletech.github.com/greeker.py/",
      install_requires=["inflect>=0.2.1", "lxml>=2.3.2", "nltk>=2.0.1rc2-git", "numpy", "argparse"],
      py_modules=['greeker'],
      scripts=['greeker.py'],
      )
