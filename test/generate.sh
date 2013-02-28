# poor man't testing
#
set -eu
../greeker.py sample1.xml 1klein.xml
../greeker.py sample2.xml 2klein.xml
../greeker.py sample3.xml 3klein.xml
../greeker.py --piglatin sample1.xml 1piglatin.xml
../greeker.py --piglatin sample2.xml 2piglatin.xml
../greeker.py --piglatin sample3.xml 3piglatin.xml
xmllint --noout *.xml
git diff *.xml
