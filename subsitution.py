import english_check
import random

# Character to number: a=0, ..., z=25
def ctn(char):
    return ord(char) - ord('a')

# Given a string and a list of alphabetic substitutions, return a new string with
# each letter of the old string substituted with the new letter
def substitute(string, substitutions):
    new_string = list(string)
    for i in range(26):
        for letter in range(len(string)):
            if string[letter] == chr(i + 97):
                new_string[letter] = chr(substitutions[i] + 97)
    return "".join(new_string)

# VERY stupid bogo brute force (does not guarantee every substitution combo will be tested...)
# def brute_force(string):
#     print("Starting brute force...")
#     subs = list(range(26))
#     for i in range(2**22):
#         if(i % 10000 == 0 and i != 0):
#             print("Combinations tried: ", i, " (", 100*i / float(10**26), "%)", sep="")
#         random.shuffle(subs)
#         new_string = substitute(string, subs)
#         sqr_freq = english_check.squared_eng_freq(new_string)

#         if abs(sqr_freq - 0.065) < 0.005:
#             print("squared_eng_freq:", sqr_freq)
#             print(subs)
#             print(new_string[:42], "\n")
#     print("Done brute force")

if __name__ == "__main__":
    string = ""
    file = open("encrypted/4.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")

    OBS = english_check.sort_dictionary(english_check.calc_observed_freq(string))
    ENG = [('e', 0.1288623426065769), ('t', 0.09024664994930598), ('a', 0.08064249900208098), ('o', 0.07378315126621263), ('n', 0.06984975410235668), ('i', 0.06905550211598431), ('s', 0.063817324270356), ('r', 0.06156572691936394), ('h', 0.06098726796371807), ('d', 0.04328667139002636), ('l', 0.04101676132771116), ('u', 0.0278568510204016), ('c', 0.026892340312538593), ('m', 0.02500971934780021), ('f', 0.0244847137116921), ('w', 0.021192261444145363), ('g', 0.019625534749730816), ('y', 0.01806326249861108), ('p', 0.017031440203182008), ('b', 0.015373768624831691), ('v', 0.010257964235274787), ('k', 0.006252182367878119), ('x', 0.0016941732664605912), ('j', 0.0011176940633901926), ('q', 0.0010648594165322703), ('z', 0.0009695838238376564)]

    subs = [None] * 26
    for index in range(26):
        i = ctn(ENG[index][0])
        subs[i] = ctn(OBS[index][0])

    print(subs)
    new = substitute(string, subs)
    print(substitute(string, subs))
    print(english_check.squared_eng_freq(new))