import re
import sys
from typing import List, Dict


# The run time complexity is O(n) because assuming that the file size is n,
# it will only iterate through the text once and split the text
# into alphanumeric subsets.
def tokenize(TextFilePath: str) -> List[str]:
    res = []
    with open(TextFilePath, 'r') as file:  # Ed disc mentioned to not use file.open, reading lines is more efficient
        for line in file:  # All the line adds up to n, so a total of o(n) for all the lines
            text = line.upper()  # case-sensitive
            # print(text)
            res += re.findall(r'[a-zA-Z0-9]+', text)  # find all the text with 1 or more upper char, and #s
            # print(res)
    return res


# The run time complexity is O(n) because it simply iterates over the input list once and count
# as each element is added or incremented in the map
def compute_word_frequencies(input: List[str]) -> Dict[str, int]:
    res = {}
    for x in input:
        res[x] = res.get(x, 0) + 1  # Increment the counter by 1 and set the default to 0 if not in map
    # print(res)
    return res


# The run time complexity is o(nlogn) because it utilizes a built-in sort method for
# a time complexity of o(nlogn) and then the program iterates through the list only once to print for a total of o(n)
def print_frequencies(input: Dict[str, int]) -> None:
    res = sorted(input.items(), key=lambda x: (-x[1], x[0]))
    # print(res)
    # sort the dictionary items by the counter in reverse order and then by the alphanumeric order of each token
    for token, count in res:  # O(n)
        print(f"{token} = {count}")


if __name__ == "__main__":
    # get file path from the command line:
    if len(sys.argv) != 2:
        print("Please input one file path")
    else:
        try:
            print_frequencies(compute_word_frequencies(tokenize(sys.argv[1])))
        except FileNotFoundError:  # if the file not found
            print(f"File not found.")
