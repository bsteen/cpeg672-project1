import operator

# Sorts the dictionary by frequency, from high to low
# Returns it as a list of tuples
def sort_dictionary(dic):
    return sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

# Helper fucntin used by squared_obs_freq and squared_eng_freq
# Calculates the frequency of each letter in a string
# Returns a dictionary with a letter/percent pair
def calc_observed_freq(string):
    freq ={'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}
    for key in freq:
        freq[key] = string.count(key) / float(len(string))
    return freq

# Calculates the frequency of the top 20 bigrams in the English language
# Returns results as dictionary
# Source https://www3.nd.edu/~busiforc/handouts/cryptography/Letter%20Frequencies.html#bigrams
def calc_bigram_freq(string):
    obs_freq ={"th":0.0, "he":0.0, "in":0.0, "er":0.0, "an":0.0, "re":0.0, "nd":0.0, "on":0.0, "en":0.0, "at":0.0, "ou":0.0, "ed":0.0, "ha":0.0, "to":0.0, "or":0.0, "it":0.0, "is":0.0, "hi":0.0, "es":0.0, "ng":0.0}
    eng_freq ={"th":0.03882543, "he":0.03681391, "in":0.02283899, "er":0.02178042, "an":0.02140460, "re":0.01749394, "nd":0.01571977, "on":0.01418244, "en":0.01383239, "at":0.01335523, "ou":0.01285484, "ed":0.01275779, "ha":0.01274742, "to":0.01169655, "or":0.01151094, "it":0.01134891, "is":0.01109877, "hi":0.01092302, "es":0.01092301, "ng":0.01053385}

    total_bigrams = len(string) - 1
    for key in obs_freq:
        obs_freq[key] = string.count(key) / float(total_bigrams)
    return obs_freq

# Calculates the frequency of each letter in a string and then multiplies each frequency by itself
# A plain English sentence should result in a value around 0.065
def squared_obs_freq(string):
    obs_freq = calc_observed_freq(string)
    sum_f_squared = 0.0
    for key in obs_freq:
        sum_f_squared += obs_freq[key] * obs_freq[key]
    return sum_f_squared

# Same as squared_obs_freq, but instead of squaring the observed frequency with
# itself, it squares the observed frequency with the actual English letter frequency
# Source: https://gist.github.com/AndyNovo/95644b26155b0ed2c879ce4ebe601819#file-frequency-py
def squared_eng_freq(string):
    english_frequency = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
    obs_freq = calc_observed_freq(string)
    sum_f_squared = 0.0
    for key in obs_freq:
        sum_f_squared += obs_freq[key] * english_frequency[key]
    return sum_f_squared

# Search a string for common words
# Returns the amount of words it found, along with the words it looked for
def found_common_word(string):
    common_words = ["the", "and", "that", "have", "for", "not", "with", "this"]
    found = 0;
    for word in common_words:
        if string.find(word) != -1:
            found += 1

    return found, len(common_words)