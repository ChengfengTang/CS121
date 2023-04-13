import sys
import partA


#  the run time complexity should be o(n + m + min(n,m)) which is simplified to o(n+m)
#  because
#  assuming that the size of file 1 is n, and the size of file2 is m
#  the program first takes input from file 1 which is o(n)
#  and then takes input from file 2 which is o(m)
#  and then it needs to iterate through the smaller set
#  and checks whether it is in the larger set
#  Overall, the run time complexity should be o(n + m + min(n,m)) which is simplified to o(n+m)
def intersection_of_two_file(TextFilePath1: str, TextFilePath2: str) -> int:
    token1 = partA.tokenize(TextFilePath1)  # o(n)
    token2 = partA.tokenize(TextFilePath2)  # o(m)
    return len(set(token1).intersection(set(token2)))  # o(min(n,m)), set gets rid of all the duplicates


if __name__ == "__main__":
    # get file paths from the command line:
    if len(sys.argv) != 3:
        print("Please input two file paths")
    else:
        try:
            print(intersection_of_two_file(sys.argv[1], sys.argv[2]))
        except FileNotFoundError:  # if the file not found
            print(f"File not found.")
