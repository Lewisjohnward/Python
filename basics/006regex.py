"""
search returns a Match object if there is a match anywhere within the string

    txt  = "helo tst"
    x = re.search("tst", txt) 
    print(x)
    <re.Match object; span=(5, 8), match='tst'>

findall returns a list containing all matches

    x = re.findall("tst", txt)
    print(x)
    ['tst']

split returns a list where the string has been split at each match

    txt = "helo tst"
    x = re.split(" ", txt)
    print(x)
    ['helo', 'tst']

sub replaces the matches with the text of your choice

    txt = "helo tst"
    x = re.sub("lo", "llo", txt)
    print(x)
    hello tst
"""

import re

string = "hello this is my string"
string = re.split(" ", string)
print(string)


