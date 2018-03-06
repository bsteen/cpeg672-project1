import itertools
import multiprocessing
import english_check

# Creates a list of tuples containing all possible permutations of column positions
def generate_column_permutations(k):
    indexes = range(k)
    # Number of permutations is k!
    return list(itertools.permutations(indexes, k))

# Calculate the total number of rows in the key
# i.e. the max length of a column; length of string ceiling dividend by the number of columns
def calc_num_rows(string, k):
    return -(-len(string) // k)

# Calculates the length of each column
# Returns lengths as list
def calc_col_lens(string, k):
    column_lengths = []

    for c in range(k):
        col_len = calc_num_rows(string, k) - 1  # All columns with be at least this long
        if len(string) % k - c > 0:             # Calculates if a column has a letter in the last row
            col_len += 1
        column_lengths.append(col_len)

    return column_lengths

# String is the raw input
# k is the number of columns
# column_lengths is a list containing the length of each column (constant for a given string and k)
# new_positions is a list containing a single permutation of column positions
# Creates a string by creating a column transposition grid and reversing the cipher
def generate_string(string, k, column_lengths, new_positions):
    rearranged_columns = [None] * k
    start = 0

    # Using the arguments, arrange the columns into the new permutation positions
    for i in range(k):
        column_pos = new_positions[i]
        length = column_lengths[column_pos]
        rearranged_columns[column_pos] = string[start: start + length]
        start += length

    # Using the new permutation, generate the string
    output_string = ""
    for i in range(len(rearranged_columns[0])):     # First column will always have the max amount of rows
        for col in rearranged_columns:              # Go through each column and append the ith character
            if i < len(col):
                output_string += col[i]

    return output_string

# The process worker function; Goes through its allotment of column position permutations,
# filters out the best results using various English fitness score methods
def test_permutations(string, k, column_lengths, column_positions):
    for permutation in column_positions:
        new_string = generate_string(string, k, column_lengths, permutation)

        # Find the most common trigrams
        trigram_freq = english_check.calc_trigram_freq(new_string)

        # Get the top trigrams; don't need their frequencies
        trigrams_only = []
        for i in range(10):
            trigrams_only.append(trigram_freq[i][0])

        # If "the" and "and" appear in the top trigrams, print the results
        if "the" in trigrams_only and "and" in trigrams_only:
            print(str(permutation) + " " + new_string)

# Launches the specified amount of process with equal workload to break the column transposition cipher
def start_brute_force(string, k, column_lengths, column_positions, num_procs):
    processes = []
    num_permutations = len(column_positions)
    print("Total number of permutations to test:", num_permutations, "")

    for pid in range(num_procs):
        start_idx = (num_permutations // num_procs) * pid
        end_idx = (num_permutations // num_procs) * pid + (num_permutations // num_procs)

        new_proc = multiprocessing.Process(target = test_permutations, args = (string, k, column_lengths, column_positions[start_idx:end_idx]))
        processes.append(new_proc)

        print("Starting process", pid, "for range:", start_idx, end_idx - 1)
        new_proc.start()

    # Wait for all processes to finish
    for proc in processes:
        proc.join()
    print("All permutations processed")

if __name__ == "__main__":
    input_string = ""
    file = open("encrypted/3.txt", "r")

    for line in file:
        input_string += line.strip().replace(" ", "")
    input_string = input_string.lower()

    # k is the number of columns
    # k can be 8, 9, or 10 for this problem
    k = 9
    print("k =", k)

    column_lengths = calc_col_lens(input_string, k)
    column_positions = generate_column_permutations(k)
    start_brute_force(input_string, k, column_lengths, column_positions, 4)
