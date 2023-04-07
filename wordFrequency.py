from typing import List, Dict
import re


def tokenize(TextFilePath: str) -> List[str]:
    try:
        f = open(TextFilePath, 'r')  # open the file for read only
        text = f.read()
        text = text.upper()  # Non case sensitive
        res = re.findall(r'[a-zA-Z0-9]+', text)  # find all the text with 1 or more upper char, and #
        #print(res)
        return res

    except FileNotFoundError:  # if the file not found
        print(f"File not found at {TextFilePath}.")

def compute_word_frequencies(input: List[str]) -> Dict[str, int]:
    res = {}
    for x in input:
        res[x] = res.get(x, 0) + 1 #Increment the counter by 1 and set the default to 0 if not in map
    return res

def print_frequencies(input: Dict[str, int]) -> None:
    res = sorted(input.items(), key = lambda x: (-x[1], x[0]))
    # sort the dictionary items by the counter in reverse order and then by the alphanumeric order of each token
    #print(res)
    for token, count in res:
        print(f"{token} = {count}")

# test:
#print_frequencies(compute_word_frequencies(tokenize('/Users/chengfeng/Desktop/input.txt')))
