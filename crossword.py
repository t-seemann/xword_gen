import os
import argparse
import pathlib

from brute_force_xword_gen import BruteForceXWordGenerator


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("wordlist", type=pathlib.Path, help="Path to wordlist")
    parser.add_argument("-o", "--output", choices=["stdout", "file"], default="stdout")

    args = parser.parse_args()

    words = loadWordList(args.wordlist)

    crossword = createCrossword(words)

    output(args.output, crossword)


def createCrossword(words):
    term_size = os.get_terminal_size()
    generator = BruteForceXWordGenerator(int(term_size.columns / 2), term_size.lines)

    return generator.generate(words)


def loadWordList(path):
    with open(path, encoding="utf-8") as file:
        read_data = file.read()
        words = read_data.splitlines()
        return words


def output(target, crossword):
    if (target == 'stdout'):
        for line in crossword:
            for char in line:
                print("{} ".format(char), end='')
            print()
    elif (target == 'file'):
        print("Not implemented!")
        print(crossword)
    else:
        print("Unkown target type")


if __name__ == "__main__":
    main()

