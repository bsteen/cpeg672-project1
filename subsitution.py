import english_check
import itertools

# Character to number: a=0, ..., z=25
def ctn(char):
    return ord(char) - ord('a')

# Number to character
def ntc(number):
    return chr(number + ord('a'))

# Given a string and a list of alphabetic substitutions, return a new string with
# each letter of the old string substituted with the new letter
def substitute(string, substitutions):
    new_string = list(string)
    for i in range(len(string)):
        new_string[i] = substitutions[ctn(new_string[i])]
    print("".join(new_string))

if __name__ == "__main__":
    string = ""
    file = open("encrypted/4.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")

    # Compare observed frequencies with actual letter frequencies
    obs_letter_freq = english_check.sort_dictionary(english_check.calc_observed_freq(string))
    print("Letter frequencies:\n", obs_letter_freq, "\n")

    obs_bigram_freq = english_check.calc_bigram_freq(string)
    print("Bigram frequencies:\n", obs_bigram_freq, "\n")

    obs_trigram_freq = english_check.calc_trigram_freq(string)
    print("Trigram frequencies:\n", obs_trigram_freq, "\n")