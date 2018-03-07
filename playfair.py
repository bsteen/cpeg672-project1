import english_check
import random

# Given an input key string, creates a list of lists that is used
# to encode or decode a message with the playfair cipher
# Returns a list of lists; Each sub list contains a row
def generate_board(key_string):
    extended_key_string = key_string.replace('j','i') + "abcdefghiklmnopqrstuvwxyz"
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
    print()

# Returns a dictionary of the row and column of each letter
def get_letter_indexes(board):
    indexes = {}
    for r in range(5):
        for c in range(5):
            indexes[board[r][c]] = r,c
    return indexes

# Check to see if 2 letter cooridnates are in the same column
def is_vertical(coord0, coord1):
    return coord0[1] == coord1[1]

# Check to see if 2 letter cooridnates are in the same row
def is_horizontal(coord0, coord1):
    return coord0[0] == coord1[0]

# Given a cipher text and a playfair board, decode the string
def decode_with_board(cipher_text, board):
    decoded_string = ""
    indexes = get_letter_indexes(board)

    # Go though ever letter pair in the cipher text
    for i in range(0, len(cipher_text), 2):
        l0_idx = indexes[cipher_text[i]]        # Index of the first letter
        l1_idx = indexes[cipher_text[i + 1]]    # Index of the second letter
        decoded_l0 = ''                         # Decoded letter corresponding to l0
        decoded_l1 = ''                         # Decoded letter corresponding to l1

        # Do the reverse of playfair encoding
        if is_vertical(l0_idx, l1_idx):     # Shift up a row
            decoded_l0 = board[(l0_idx[0] - 1) % 5][l0_idx[1]]
            decoded_l1 = board[(l1_idx[0] - 1) % 5][l1_idx[1]]
        elif is_horizontal(l0_idx, l1_idx): # Shift left a column
            decoded_l0 = board[l0_idx[0]][(l0_idx[1] - 1) % 5]
            decoded_l1 = board[l1_idx[0]][(l1_idx[1] - 1) % 5]
        else:                               # Use opposite corner, same row
            decoded_l0 = board[l0_idx[0]][l1_idx[1]]
            decoded_l1 = board[l1_idx[0]][l0_idx[1]]

        decoded_string += decoded_l0 + decoded_l1

    return decoded_string

# Swaps the location of two letter
# Takes in coordinates of the letters to be swapped and the board
def swap_letters(l0r, l0c, l1r, l1c, board):
    temp = board[l0r][l0c]
    board[l0r][l0c] = board[l1r][l1c]
    board[l1r][l1c] = temp
    return board

def shotgun_hill_climb(cipher_text, board):
    sqr_eng_freq = english_check.squared_eng_freq(cipher_text)
    best_error = abs(sqr_eng_freq - 0.065)
    best_board = board
    best_decode = decode_with_board(cipher_text, best_board)
    count = 0

    while best_error > 0.001 and count < 200000:
        coords = []
        decoded_text = ""

        for n in range(4):
            coords.append(random.randint(0, 4))

        board = swap_letters(coords[0], coords[1], coords[2], coords[3], board)
        decoded_text = decode_with_board(cipher_text, board)
        sqr_eng_freq = english_check.squared_eng_freq(decoded_text)

        if abs(sqr_eng_freq - 0.065) < best_error:
            best_error = abs(sqr_eng_freq - 0.065)
            best_board = board
            best_decode = decoded_text
        else:
            board = swap_letters(coords[0], coords[1], coords[2], coords[3], board)

        count += 1
        if count % 10000 == 0:
            print("Number of boards tried:", count)
            print("Best error so far:", best_error, "\n")

    print("Number of boards tried:", count)
    print_board(best_board)
    print("Decoded text:", best_decode)

if __name__ == "__main__":
    string = ""
    file = open("encrypted/2.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")
    cipher_text = string.lower()

    # obs_bigram_freq = english_check.calc_bigram_freq(string)
    # print("Bigram frequencies:\n", obs_bigram_freq, "\n")

    board = generate_board("abcdefghiklmnopqrstuvwxyz")
    print_board(board)
    shotgun_hill_climb(cipher_text, board)