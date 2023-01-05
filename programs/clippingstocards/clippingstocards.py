"""
    This program creates importable Anki cards from My Clippings.txt file created by
    Kindle when highlighting text
"""

# for regex
import re

# Open file and read all txt
filename = "My Clippings.txt"

# If unable to open file exit program
try:
    with open(filename):
        clippings = open(filename).read()
except IOError:
    print(f'Unable to open {filename} are you sure the program is being called in the same directory')
    exit()

clippings = re.split("\n", clippings)

cards = open("cards.txt", "w")

i = 0
sources= {}

for line in clippings:
    if i == 0:
        # Move line along one to remove <feff> if present
        # Make sure that line has characters before comparison
        if len(line) != 0 and ord(line[0]) == 65279:
            title = line[1:]
        else:
            title = line

    if i == 3:
        text = f'{line}'

    i += 1
    if i == 5:
        # Update sources
        if title in sources:
            sources[title] += 1
        else:
            sources[title] = 1
        # Write line to file
        cards.write(f'"{title}<hr>{text}";\n')
        i = 0

# Prints stats
count = 0
for source in sources:
    count += sources[source]
print(f'Cards created: {count}')

for source in sources:
    print(f'{source} : {sources[source]}')
