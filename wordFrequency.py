
from typing import List, Dict

class Token:
    #Token is a sequence of alphanumeric characters, independent of capitalization
    text = ''


def tokenize(TextFilePath: str) -> List[Token]:
    f =  open(TextFilePath, 'r')
    text = f.read()
    #print(text)
    res = []
    for x in text:
        print(x)

#test:
tokenize('/Users/chengfeng/Desktop/input.txt')
