import itertools
import numpy as np
import time
import multiprocessing
import english_check

# Character to number: a=0, ..., z=25
def ctn(char):
    return ord(char) - ord('a')

# Number to character
def ntc(number):
    return chr(number + ord('a'))

# Convert a string in a list of 2x1 vectors
def string_to_vec(string):
    s = string
    if len(s) % 2 != 0:
        s += 'x'

    vec_list = []
    for i in range(0, len(s), 2):
        a = [ctn(s[i])]
        b = [ctn(s[i+1])]
        vec = np.matrix([a,b])
        vec_list.append(vec)

    return vec_list

# Convert a tuple of 4 to a numpy 2x2 matrix
# Used by gen_all_key_matrixes
def tuple_to_2x2(tup):
    row_1 = list(tup[0:2])
    row_2 = list(tup[2:4])
    return np.matrix([row_1, row_2])

# Generate all possible key matrixes for a 2x2 hill
# Returns a list of 2x2 matrixes
def gen_all_key_matrixes():
    print("Generating all key combination tuples...")
    alphabet = list(range(26))
    key_list = list(itertools.permutations(alphabet, 4))    # 26×25×24×23 = 358800 possible keys

    print("\tDone\nConverting all key combination tuples to matrixes...")
    # Convert the list of tuples to a list of matrixes
    key_matrix_list = []
    for lst in key_list:
        key_matrix_list.append(tuple_to_2x2(lst))

    print("\tDone")
    return key_matrix_list

# Takes in a key matrix and a string in the form of a list of 2x1 vectors
# Decodes the string and tests to see if could be valid English
def test_key(matrix_key, vector_string):
    decoded = ""

    # Perform the matrix multiplication and convert the result back to characters
    for vec in vector_string:
        vec_result = (matrix_key * vec) % 26
        decoded += ntc(vec_result[0][0]) + ntc(vec_result[1][0])

    # Check if the decoded string is plain text English
    sqr_eng_sum = english_check.squared_eng_freq(decoded)
    if abs(sqr_eng_sum - 0.065) < 0.004:
        return True, sqr_eng_sum, decoded
    else:
        return False, sqr_eng_sum, decoded

# Worker function for a process; Used by test_all_keys_parallel
# Each process outputs its results to output/hill2x2_pid
# Each process will ocassioanly output its current progress to the terminal
def proc_worker(key_set, vector_string, start, end, pid):
    print("Starting process " +  str(pid) + "; Range: " + str(start) + " " +  str(end - 1))
    output_file = open("output/hill2x2_" + str(pid), "w")
    output_file.writelines("Process: " + str(pid) + "\nRange: " + str(start) + " " + str(end - 1) + "\n\n")

    count = 0
    for key in key_set:
        text_check, sqr_eng_sum, decoded = test_key(key, vector_string)
        if text_check:
            output_file.writelines("Tested key:\n"+ str(key) + "\nEnglish Frequency Sums Squared: " + str(sqr_eng_sum) + "\nDecoded text: " + decoded + "\n\n")

        count += 1
        if count % 1000 == 0:
            print("Process " + str(pid) + " keys tested: " + str(count) + "/" + str(len(key_set)))

    output_file.close()
    print("Process " + str(pid) + " finished range: " + str(start) + " " + str(end))
    return

# Tests all possible keys by launching multiple process and dividing up the work evenly among them
def test_all_keys_parallel(keys, vector_string, num_procs):
    num_keys = len(keys)
    processes = []
    print("Testing all", num_keys, "keys with", num_procs, "processes...")

    for pid in range(num_procs):
        start_idx = (num_keys // num_procs) * pid
        end_idx = (num_keys // num_procs) * pid + (num_keys // num_procs)
        new_proc = multiprocessing.Process(target = proc_worker, args = (keys[start_idx:end_idx], vector_string, start_idx, end_idx, pid))
        processes.append(new_proc)
        new_proc.start()

    # Main process blocks until all processes are finished
    for proc in processes:
        proc.join()

    print("Done testing all keys\n")
    return

if __name__ == "__main__":
    string = ""
    file = open("encrypted/5.txt", "r") # 5.txt has 588 characters

    for line in file:
        string += line.strip().replace(" ", "")
    string = string.lower()

    multiprocessing.set_start_method('spawn')
    vector_string = string_to_vec(string)           # Convert the string into sets of 2x1 vectors

    # Run these 2 lines to find all relatively possible keys and there decoded solutions
    # keys = gen_all_key_matrixes()                   # Generate all permutations of a 2x2 key
    # test_all_keys_parallel(keys, vector_string, 4)  # Brute force with multiple processes

    # Now look through the output files and find the key that worked... (found in hill2x2_14 when using 24 processes)
    # Run these lines when you know the correct key
    matrix_key = np.matrix([[15,13],[9,24]])    # Correct key goes here
    print("Tested key:\n", matrix_key)
    decoded = test_key(matrix_key, vector_string)[2]
    print("English Frequency Sums Squared:", english_check.squared_eng_freq(decoded))
    print("Decoded text:", decoded)