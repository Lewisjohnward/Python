"""
    Takes a dir and creates a csv with images ready to be imported into Anki
"""


from pathlib import Path
import re
import sys

title = sys.argv[1]

entries = Path(sys.argv[2])

hr = "<hr>"

cards = open("cards.txt", "w")
for entry in entries.iterdir():
    filepath = re.sub('.*?/', '', str(entry))
    cards.write(f'{title}{hr}<img src="{filepath}" />;\n')
