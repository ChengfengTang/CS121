import sys
import partA


#  the run time complexity should be o(min(n,m)) because the program only needs to iterate through the smaller set
#  and checks whether it is in the larger set
def intersection_of_two_file(TextFilePath1: str, TextFilePath2: str) -> int:
    token1 = partA.tokenize(TextFilePath1)  # o(n)
    token2 = partA.tokenize(TextFilePath2)  # o(m)
    return len(set(token1).intersection(set(token2)))  # set gets rid of all the duplicates


if __name__ == "__main__":
    # get file paths from command line:
    if len(sys.argv) != 3:
        print("Please input two file paths")
    else:
        try:
            print(intersection_of_two_file(sys.argv[1], sys.argv[2]))
        except FileNotFoundError:  # if the file not found
            print(f"File not found.")
