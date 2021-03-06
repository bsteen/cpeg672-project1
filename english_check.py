import operator

# Sorts the dictionary by frequency, from high to low
# Returns it as a list of tuples
def sort_dictionary(dic):
    return sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

# Helper function used by squared_obs_freq and squared_eng_freq
# Calculates the frequency of each letter in a string
# Returns a dictionary with a letter/percent pair
def calc_observed_freq(string):
    freq ={'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}
    for key in freq:
        freq[key] = string.count(key) / float(len(string))
    return freq

# Calculates the frequency of the bigrams
# Returns results as a list of the top 20, from high to low frequency
def calc_bigram_freq(string):
    obs_freq = {}
    total_bigrams = len(string) - 1

    for i in range(0, total_bigrams):
        bigram = string[i:i+2]
        obs_freq[bigram] = string.count(bigram)
    for key in obs_freq:
        obs_freq[key] = obs_freq[key] / float(total_bigrams)

    return sort_dictionary(obs_freq)[:20]

# Calculates the frequency of the trigrams
# Returns results as a list of the top results, from high to low frequency
def calc_trigram_freq(string):
    obs_freq = {}
    total_trigrams = len(string) - 2

    for i in range(0, total_trigrams):
        trigram = string[i:i+3]
        obs_freq[trigram] = string.count(trigram)
    for key in obs_freq:
        obs_freq[key] = obs_freq[key] / float(total_trigrams)

    return sort_dictionary(obs_freq)[:20]

# Out of all 2 letter pairs, count pairs of duplicate letters (aa, bb, cc ...)
# Returns results as a list of the top results, from high to low frequency
def duplicate_letter_count(string):
    obs_freq = {}
    letter_pairs = len(string) - 1

    for i in range(26):
        letter = chr(i + ord('a'))
        obs_freq[letter] = string.count(letter + letter)

    return sort_dictionary(obs_freq)

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
# Returns a tuple of the amount of words it found with the number of words it looked for
def found_common_word(string):
    common_words = ["the", "and", "that", "have", "for", "not", "with", "this"]
    found = 0
    for word in common_words:
        if string.find(word) != -1:
            found += 1

    return found, len(common_words)