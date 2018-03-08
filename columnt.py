import itertools
import multiprocessing
import time
import english_check

# Calculate the total number of rows in the key
# i.e. the max length of a column; length of string ceiling dividend by the number of columns
def calc_num_rows(string, k):
    return -(-len(string) // k)

# Calculates the length of each column
# Returns lengths as a list
def calc_col_lens(string, k):
    # All columns will be at least this long
    column_lengths = [calc_num_rows(string, k) - 1] * k

    # Determine how many characters are in the last row (does a column have a letter in the last row?)
    last_row_length = len(string) % k
    if last_row_length == 0:
        last_row_length = k

    # Add one more to each column's length as needed
    for c in range(last_row_length):
        column_lengths[c] += 1

    return column_lengths

# Creates a list of tuples containing all possible permutations of column positions
def generate_column_permutations(k):
    indexes = range(k)
    # Number of permutations is k!
    return list(itertools.permutations(indexes, k))

# String is the raw input text
# k is the number of columns
# column_lengths is a list containing the length of each column (constant for a given string and k)
# new_positions is a tuple containing a single permutation of the possible column positions
# Creates a string by creating a column transposition grid and reversing the cipher
def generate_string(string, k, column_lengths, new_positions):
    rearranged_columns = [None] * k
    start = 0

    # Using the arguments, arrange the columns into the new permutation positions
    for i in range(k):
        column_pos = new_positions[i]
        length = column_lengths[column_pos]
        rearranged_columns[column_pos] = string[start: start + length]  # Using the precalculated column lengths, this makes sure each column has the correct amount of letters
        start += length

    # Using the columns, generate the string
    output_string = ""
    for i in range(len(rearranged_columns[0])):     # First column will always have the max amount of rows
        for col in rearranged_columns:              # Go through each column and append the ith character
            if i < len(col):
                output_string += col[i]

    return output_string

# The process worker function; Goes through its allotment of column position permutations,
# filters out the best results using various English fitness score methods
def test_permutations(string, k, column_lengths, column_positions):
    time.sleep(0.5) # Wait for other processes to start
    for permutation in column_positions:
        new_string = generate_string(string, k, column_lengths, permutation)

        # Find the most common trigrams
        trigram_freq = english_check.calc_trigram_freq(new_string)

        # Get the top 5 trigrams; don't need their frequencies
        top_trigrams = []
        for i in range(10):
            top_trigrams.append(trigram_freq[i][0])

        # If "the" and "and" appear in the top trigrams, print the results
        # if "the" in top_trigrams and "and" in top_trigrams:
        #     print(str(permutation) + ": " + new_string[:60])

        # Based on the trigram filtering I used above, the phrase "itsnothing" seems to appear in the decoded text
        if new_string.find("itsnothing") != -1:
            print(str(permutation) + ": " + new_string[:60])

# Launches the specified amount of process with equal workload to brute force the column transposition cipher
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
    k = 10
    print("k =", k)
    column_lengths = calc_col_lens(input_string, k)

    # Run these two commands when trying to find the correct column transposition
    # column_positions = generate_column_permutations(k)
    # start_brute_force(input_string, k, column_lengths, column_positions, 4)

    # When you know the column transposition that works, run these lines below:
    column_position = (6, 8, 2, 4, 1, 7, 3, 5, 9, 0)
    print("Column transposition:", column_position)
    print("Decoded text:", generate_string(input_string, k, column_lengths, column_position))