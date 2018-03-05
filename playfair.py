import english_check
import numpy as np

# Given an input key string, creates a list of lists that is used
# to encode or decode a message with the playfair cipher
def generate_board(raw_key_string):
    extended_key_string = raw_key_string.replace('j','i') + "abcdefghiklmnopqrstuvwxyz"
    key = sorted(set(extended_key_string), key=extended_key_string.index)     # Remove duplicate letters and maintain original order

    # Convert key_string into the board
    board = []
    for row in range(0,21,5):
        board.append(key[row:row+5])

    return board

def print_board(board):
    print("Showing board:")
    for r in board:
        for c in r:
            print(c, end="")
        print()

if __name__ == "__main__":
    string = ""
    file = open("encrypted/2.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")
    string = string.lower()

    obs_bigram_freq = english_check.calc_bigram_freq(string)
    print("Bigram frequencies:\n", obs_bigram_freq, "\n")

    # board = generate_board("playfairexample")
    # print_board(board)