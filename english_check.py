letter_frequency = {'a': 0.080642499002080981, 'c': 0.026892340312538593, 'b': 0.015373768624831691, 'e': 0.12886234260657689, 'd': 0.043286671390026357, 'g': 0.019625534749730816, 'f': 0.024484713711692099, 'i': 0.06905550211598431, 'h': 0.060987267963718068, 'k': 0.0062521823678781188, 'j': 0.0011176940633901926, 'm': 0.025009719347800208, 'l': 0.041016761327711163, 'o': 0.073783151266212627, 'n': 0.069849754102356679, 'q': 0.0010648594165322703, 'p': 0.017031440203182008, 's': 0.063817324270355996, 'r': 0.06156572691936394, 'u': 0.027856851020401599, 't': 0.090246649949305979, 'w': 0.021192261444145363, 'v': 0.010257964235274787, 'y': 0.01806326249861108, 'x': 0.0016941732664605912, 'z': 0.0009695838238376564}
total_percent = 1.0000000000000002

# Used to calculate the total value of letter_frequency
# Should be 1.00; Actual value stored in total_percent
# def calc_total_percent():
#     total = 0
#     for key in letter_frequency:
#           total += letter_frequency[key]
#     print(total)

# Given a string, calculate the frequency of each letter
# Returns a dictionary of letters with a percent
def calc_letter_freq(string):
    let_freq ={'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0}
    total_letters = 0

    for i in string:
        if i in let_freq:
            let_freq[i] += 1
            total_letters += 1

    for key in let_freq:
       let_freq[key] = (let_freq[key] / total_letters)

    return let_freq

# A plain text or substitution cipher string should be close to 0.065
# Squares the frequency of a letter with itself
def calc_squared_sum(string):
    calculated_freq = calc_letter_freq(string)
    sum_f_squared = 0.0
    sum_f = 0.0
    for key in calculated_freq:
        sum_f += calculated_freq[key]
        sum_f_squared += calculated_freq[key]**2

    return sum_f_squared

# Used to detect whether a shift in letters potentially made the text plain English
# Squares the frequency of a letter with the standard English frequency
# Returns True if the sum of the frequncies is within 0.5% of 0.065 by default
def shift_fix_detect(shifted_string, error = .005):
    shift_str_freq = calc_letter_freq(shifted_string)

    sum_f_sqr = 0.0
    for key in shift_str_freq:
        sum_f_sqr += shift_str_freq[key] * letter_frequency[key]

    return abs(sum_f_sqr - .065) < error

# Search a string for common words
# Returns the amount of words it found, along with the words it looked for
def found_common_word(string):
    common_words = ["the", "and", "that", "have", "for", "not", "with", "this"]
    found = 0;
    for word in common_words:
        if string.find(word) != -1:
            found += 1

    return found, len(common_words)