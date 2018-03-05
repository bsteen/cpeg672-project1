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
    print("Decoded text:", "".join(new_string), "\n")

if __name__ == "__main__":
    string = ""
    file = open("encrypted/4.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")

    # Compare observed frequencies with actual letter frequencies
    obs_letter_freq = english_check.sort_dictionary(english_check.calc_observed_freq(string))
    print("Observed letter frequencies:\n", obs_letter_freq, "\n")

    obs_bigram_freq = english_check.calc_bigram_freq(string)
    print("Bigram frequencies:\n", obs_bigram_freq, "\n")

    obs_trigram_freq = english_check.calc_trigram_freq(string)
    print("Trigram frequencies:\n", obs_trigram_freq, "\n")

    obs_dup_letter_freq = english_check.duplicate_letter_count(string)
    print("Duplicate letter frequencies:\n", obs_dup_letter_freq, "\n")

    # Used the above functions to guess what t, h, and e mapped to. Looked at the results and tried to create words from theses base letters
    # Trial and error to see what letters were good
    # substitute(string, ['-','-','-','e','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','h','t'])
    # substitute(string, ['-','-','-','e','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','a','-','-','-','-','h','t'])
    # substitute(string, ['r','-','-','e','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','a','-','-','-','-','h','t'])
    # substitute(string, ['r','-','-','e','-','-','-','-','-','-','-','-','c','-','-','-','-','-','-','a','-','-','-','-','h','t'])
    # substitute(string, ['r','-','-','e','-','-','-','-','-','-','-','-','c','-','-','-','-','-','-','a','-','n','-','-','h','t'])
    # substitute(string, ['r','-','-','e','-','s','-','-','-','-','-','-','c','-','-','-','-','-','-','a','-','n','-','-','h','t'])
    # substitute(string, ['r','-','-','e','-','s','-','-','-','-','-','-','c','-','-','-','i','-','-','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','-','e','-','s','-','-','-','-','-','-','c','-','-','-','i','-','-','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','-','e','-','s','-','-','-','-','-','-','c','-','-','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','-','e','-','s','-','-','-','-','-','-','c','-','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','-','e','-','s','-','-','-','-','-','-','c','g','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','-','e','-','s','-','-','-','l','-','-','c','g','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','-','s','-','-','-','l','-','-','c','g','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','-','s','d','-','-','l','-','-','c','g','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','-','s','d','-','b','l','-','-','c','g','v','-','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','-','s','d','-','b','l','-','-','c','g','v','u','i','-','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','-','s','d','-','b','l','-','-','c','g','v','u','i','j','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','f','s','d','-','b','l','-','-','c','g','v','u','i','j','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','f','s','d','-','b','l','-','w','c','g','v','u','i','j','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','f','s','d','m','b','l','-','w','c','g','v','u','i','j','y','a','-','n','-','-','h','t'])
    # substitute(string, ['r','p','o','e','f','s','d','m','b','l','-','w','c','g','v','u','i','j','y','a','-','n','-','x','h','t'])
    substitute(string, ['r','p','o','e','f','s','d','m','b','l','k','w','c','g','v','u','i','j','y','a','z','n','q','x','h','t'])
    #                  ['a','b','c','d','e','f','g','h','i','j', k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # There are no k's or w's in the cipher text and there are no k's or q's in the decoded test, so k=k,q and w=k,q