from typing import List, Dict
import re

# The run time complexity is O(n) because it will only iterate through the text once and split the text
# into alphanumeric subsets. And the other trivial operations are O(1)
def tokenize(TextFilePath: str) -> List[str]:
    try:
        f = open(TextFilePath, 'r')  # open the file for read only O(1)
        text = f.read() # O(1)
        text = text.upper()  # Non case sensitive O(1)
        #print(text)
        res = re.findall(r'[a-zA-Z0-9]+', text)  # find all the text with 1 or more upper char, and #s O(n)
        #print(res)
        return res

    except FileNotFoundError:  # if the file not found
        print(f"File not found at {TextFilePath}.")

# The run time complexity is O(n) because it simply iterates over the input list once and count
# as each element is added or incremented in the map
def compute_word_frequencies(input: List[str]) -> Dict[str, int]:
    res = {}
    for x in input:
        res[x] = res.get(x, 0) + 1  # Increment the counter by 1 and set the default to 0 if not in map
    #print(res)
    return res

# The run time complexity is o(nlogn) because it has a sort method for o(nlogn) and print method
# that iterates through the list only once for o(n)
def print_frequencies(input: Dict[str, int]) -> None:
    res = sorted(input.items(), key = lambda x: (-x[1], x[0]))
    #print(res)
    # sort the dictionary items by the counter in reverse order and then by the alphanumeric order of each token
    for token, count in res: # O(n)
        print(f"{token} = {count}")

# test:
print_frequencies(compute_word_frequencies(tokenize('/Users/chengfeng/Desktop/input.txt')))
