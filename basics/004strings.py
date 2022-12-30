#
# Accessing character at position
# 
# Loop through letters in string
#

a = "Hello"

# Accesses element in array
b = a[1]
print(b)

# Loops through letters and prints them
for x in a:
    print(x)

# Get string length
c = len(a)
print(c)

# Check if substring is present in string
d = "Hell" in a
print(d)

test = 'hello'
if d:
    # Concatenation
    print("Hell is a substring of " + a)
    # Using f strings
    print(f"Hell is a substring of {a}")
