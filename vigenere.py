import itertools
import english_check

# Shift a given charcter c by integer n
def shift_letter(c, n):
    return chr(((ord(c) + n - ord('a')) % 26) + ord('a'))

# Given a string , shift every character by shift_amount
def shift_every_letter(string, shift_amount):
    shifted_string = ""
    for letter in string:
        shifted_string += shift_letter(letter, shift_amount)
    return shifted_string

# Given a key length, find the shifts that were most likely used for each part of the key
# Returns a list of lists; Each sublist contain the most likely used shifts for that position
def find_potential_shifts(string, key_len):
    keys = []
    # Solve for each letter in key
    for i in range(0, key_len):
        # Try different shift amount
        shift_freqs = {}
        for shift in range(1, 26):
            # For a given shift amount, shift every ith character by this amount
            shifted_letters = shift_every_letter(string[i::key_len], shift)
            # Calculate the square of the frequency of the shifted letters using the standard English frequency
            shift_freqs[shift] = english_check.squared_eng_freq(shifted_letters)

        # print(shift_freqs, "\n")
        # Go through the shift_freqs and find the best shifts
        # Calculate how close the shift made the characters to normal English frequency
        best_fits = []
        for k in shift_freqs:
            if abs(shift_freqs[k] - 0.065) <= 0.017:
                best_fits.append(k)
        keys.append(best_fits)
        # print("Best shifts for position", i, ":", keys[-1])

    print("Potential key shifts found:", keys)
    return keys

# Given a list containing lists of possible shift combinations, returns a list of all permutations
def find_key_permutations(potential_shifts):
    # Check to see have man permutations will be generated
    total_combo_check = 1
    for letters in potential_shifts:
        total_combo_check *= len(letters)

    if total_combo_check >= 2**10:
        print("Warning! Keys found:", total_combo_check)
        answer = input("Do you want to continue? y/[n] ")
        if answer != "y":
            quit()

    list_of_tuples = list(itertools.product(*potential_shifts))

    list_of_lists = []
    for x in list_of_tuples:
        list_of_lists.append(list(x))


    print(len(list_of_lists), "possible key(s) found!")
    return list_of_lists

# Given a list of keys, try to solve the Vigener cipher with each key
# Note: the decode key must be the opposite of what was used to encode the message:
# E.g: Key to encode: 18,10,11,8,26,12,9,9,12,6 => key to decode: 9,17,16,19,1,15,18,18,15,21
def solve_with_keys(string, keys):
    for key in keys:
        decoded = list(string)
        for i in range(0, len(string), len(key)):
            for j in range(0, len(key)):
                if i + j < len(string):
                    decoded[i + j] = shift_letter(string[i + j], key[j])
        decoded = "".join(decoded)
        sqr_eng_freq = english_check.squared_eng_freq(decoded)

        f, w = english_check.found_common_word(decoded)
        if f == w :#and abs(sqr_eng_freq - 0.065) <= 0.005:
            print("Testing permutation:", key)
            print("\tSquared Frequency:", sqr_eng_freq)
            print("\tPrintout of first 48 characters:", decoded[:48])

if __name__ == "__main__":
    string = ""
    file = open("encrypted/challenge.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")

    key_len = 16
    print("Key length selected:", key_len)

    potential_shifts = find_potential_shifts(string, key_len)
    keys = find_key_permutations(potential_shifts)

    solve_with_keys(string, keys)