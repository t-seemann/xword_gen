from xword_gen import XWordGenerator
from dataclasses import dataclass
import random


@dataclass
class PlacedWord():
    word: str
    position_x: int
    position_y: int
    orientation: bool
    length: int


class BruteForceXWordGenerator(XWordGenerator):

    size_x: int
    size_y: int

    EMPTY_FIELD = ' '

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.crossword = [[self.EMPTY_FIELD for x in range(size_x)] for y in range(size_y)]
        self.placed_word = []

    def placeFirstWord(self, word):
        midpoint_x = int(self.size_x / 2)
        midpoint_y = int(self.size_y / 2)

        placement_x = midpoint_x
        placement_y = midpoint_y - int(word.length / 2)

        word.position_x = placement_x
        word.position_y = placement_y

        self.place_word(word)

    def place_word(self, word: PlacedWord):
        if word.position_x == -1 or word.position_y == -1:
            raise Exception("Can't place word {}".format(word))

        if word.orientation:
            for index in range(0, word.length):
                self.crossword[word.position_y][word.position_x + index] = word.word[index]
        else:
            for index in range(0, word.length):
                self.crossword[word.position_y + index][word.position_x] = word.word[index]

    def any_matching_char(self, str1: str, str2: str) -> bool:
        for c1 in str1:
            for c2 in str2:
                if c1 == c2:
                    return True
        return False

    def find_matching_word(self, word: PlacedWord):
        matches = []
        for placed_word in self.placed_word:
            if not placed_word.orientation == word.orientation:
                if self.any_matching_char(word.word, placed_word.word):
                    matches.append(placed_word)

        return matches

    def calc_possible_position(self, word: str, fixed_word: str):
        pos = []
        for index in range(0, len(fixed_word)):
            for c in word:
                if fixed_word[index] == c:
                    pos.append(index)

        return pos

    def calc_placement(self, word: PlacedWord, matching_word, pos):
        # word:          current word to be placed
        # matching_word: already present word, we want to add to
        # we have the already placed word with some orientation
        #     pos
        #      v
        #    X X X X X
        matched_char = matching_word.word[pos]
        pos_in_word = word.word.index(matched_char)

        if word.orientation:
            # Horizontal
            # y stay the same as the matched_char position
            # x is starting at pos
            crossing_x = matching_word.position_x
            crossing_y = matching_word.position_y + pos

            x = crossing_x - pos_in_word
            y = crossing_y
            return x, y, crossing_x, crossing_y
        else:
            # Vertical
            # x stay the same as the matched_char position
            # y is starting at pos
            crossing_x = matching_word.position_x + pos
            crossing_y = matching_word.position_y

            x = crossing_x
            y = crossing_y - pos_in_word
            return x, y, crossing_x, crossing_y

    def test_placement(self, placed_word, x, y, crossing_x, crossing_y):
        # go through the grid of already placed words and check depending on the
        # orientation above and below, right and left and if crossing a word
        # then check if it is the same letter.
        word = placed_word.word

        if placed_word.orientation:
            
            # Check left of the start of the word
            if x - 1 >= 0:
                if self.crossword[y][x - 1] != self.EMPTY_FIELD:
                    return False

            # Check right of the end of the word
            if x + 1 <= self.size_x:
                if self.crossword[y][x + len(word)] != self.EMPTY_FIELD:
                    return False

            for x_delta in range(0, len(word)):
                above_empty = False
                if y == 0:
                    above_empty = True
                else:
                    if x + x_delta == crossing_x:
                        above_empty = True
                    else:
                        above_empty = self.crossword[y - 1][x + x_delta] == self.EMPTY_FIELD

                below_empty = False
                if y == self.size_y:
                    below_empty = True
                else:
                    if x + x_delta == crossing_x:
                        below_empty = True
                    else:
                        below_empty = self.crossword[y + 1][x + x_delta] == self.EMPTY_FIELD

                empty_or_same = False
                if self.crossword[y][x + x_delta] != self.EMPTY_FIELD:
                    if self.crossword[y][x + x_delta] == word[x_delta]:
                        empty_or_same = True
                else:
                    empty_or_same = True

                if not (above_empty and below_empty and empty_or_same):
                    return False

            return True
        else:
            # Check above of the start of the word
            if y - 1 >= 0:
                if self.crossword[y - 1][x] != self.EMPTY_FIELD:
                    return False

            # Check below of the end of the word
            if y + 1 <= self.size_y:
                if self.crossword[y + len(word)][x] != self.EMPTY_FIELD:
                    return False

            for y_delta in range(0, len(word)):
                left_empty = False
                if x == 0:
                    left_empty = True
                else:
                    if y + y_delta == crossing_y:
                        left_empty = True
                    else:
                        left_empty = self.crossword[y + y_delta][x - 1] == self.EMPTY_FIELD

                right_empty = False
                if x == self.size_x:
                    right_empty = True
                else:
                    if y + y_delta == crossing_y:
                        right_empty = True
                    else:
                        right_empty = self.crossword[y + y_delta][x + 1] == self.EMPTY_FIELD
                
                empty_or_same = False
                if self.crossword[y + y_delta][x] != self.EMPTY_FIELD:
                    if self.crossword[y + y_delta][x] == word[y_delta]:
                        empty_or_same = True
                else:
                    empty_or_same = True 
               
                if not (left_empty and right_empty and empty_or_same):
                    return False

            return True


    def try_set_word(self, placed_word):
        if len(self.placed_word) == 0:
            self.placeFirstWord(placed_word)
            return True
        else:
            # find word with match
            matching_words = self.find_matching_word(placed_word)
            
            placed = False
            for matching_word in matching_words:
                # check if word can be placed at this position
                possible_pos = self.calc_possible_position(placed_word.word, matching_word.word)
                random.shuffle(possible_pos)
                # place word
                for pos in possible_pos:
                    x, y, crossing_x, crossing_y = self.calc_placement(placed_word, matching_word, pos)
                    if (x < 0 or y < 0):
                        continue

                    if self.test_placement(placed_word, x, y, crossing_x, crossing_y):
                        placed = True
                        placed_word.position_x = x
                        placed_word.position_y = y
                        self.place_word(placed_word)
                        break

                if placed:
                    break
                           
            return placed

    def generate(self, words):
        ori = True  # Horizontal
        previous_words = []
        for word in words:
            # Make sure we do not run into an endless loop
            if word in previous_words:
                print("loop detected")

            previous_words.append(word)

            placed_word = PlacedWord(word, position_x=-1, position_y=-1, orientation=ori, length=len(word))

            placed = self.try_set_word(placed_word)

            if not placed:
                ori = not ori
                placed_word.orientation = ori
                if self.try_set_word(placed_word):
                    self.placed_word.append(placed_word)
                else:
                    print("Could not place word {}".format(placed_word))
                    return self.crossword
            else:
                self.placed_word.append(placed_word)

            ori = not ori
            
        return self.crossword


