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

# Convert a string in a list of 2x1 matrixes (vector)
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

# Generate all keys matrixes for a 2x2 hill
# Returns a list of 2x2 matrixes
# This function takes 7-10 seconds
def gen_all_key_matrixes():
    print("Generating all key combinations...")
    alphabet = list(range(26))
    # 26×25×24×23 = 358800 possible keys
    key_list = list(itertools.permutations(alphabet, 4))

    print("\tDone\nConverting all key combinations to matrixes...")
    # Convert the list of tuples to a list of matrixes
    key_matrix_list = []
    for lst in key_list:
        key_matrix_list.append(tuple_to_2x2(lst))

    print("\tDone")
    return key_matrix_list

# Takes in a key matrix and a string in the form of a list of 2x1 vectors
# Decoded the string and tests to see if could be valid English
def test_key(matrix_key, vector_string):
    decoded = ""

    # Perform the matrix multiplication and convert the result back to characters
    for vec in vector_string:
        vec_result = (matrix_key * vec) % 26
        decoded += ntc(vec_result[0][0]) + ntc(vec_result[1][0])

    # Check if the decoded string in plain text English
    sqr_eng_sum = english_check.squared_eng_freq(decoded)
    if abs(sqr_eng_sum - 0.065) < 0.004:
        return True, sqr_eng_sum, decoded
    else:
        return False, sqr_eng_sum, decoded

# Given a list of key matrixes and an input string in the form of a list of 2x1
# vectors, test all the keys on the input string
def test_all_keys(keys, vector_string):
    print("Testing all", len(keys), "keys...")
    output_file = open("output/hill2x2.txt", "w")
    count = 1

    for key in keys:
        text_check, sqr_eng_sum, decoded = test_key(key, vector_string)
        if text_check:
            output_file.writelines("Tested key:\n"+ str(key) + "\nSquared English Frequency Sum: " + str(sqr_eng_sum) + "\nDecoded text: " + decoded + "\n\n")
        if count % 1000 == 0:
            print("Number of keys tested:", count, "/", len(keys))
        count += 1

    output_file.close()
    print("Done testing all keys")
    return

# Worker function for a process; Used by test_all_keys_parallel
def proc_worker(key_set, vector_string, start, end, pid):
    print("Starting process " +  str(pid) + "; Range: " + str(start) + " " +  str(end - 1))
    output_file = open("output/hill2x2_" + str(pid), "w")
    output_file.writelines("Process: " + str(pid) + "\nRange: " + str(start) + " " + str(end - 1) + "\n\n")

    count = 0
    for key in key_set:
        text_check, sqr_eng_sum, decoded = test_key(key, vector_string)
        if text_check:
            output_file.writelines("Tested key:\n"+ str(key) + "\nSquared English Frequency Sum: " + str(sqr_eng_sum) + "\nDecoded text: " + decoded + "\n\n")

        count += 1
        if count % 1000 == 0:
            print("Thread " + str(pid) + " number of keys tested: " + str(count) + "/" + str(len(key_set)))

    output_file.close()
    print("Process " + str(pid) + " finished range: " + str(start) + " " + str(end))
    return

# Same as test_all_keys, except does it in parallel with multiple processes
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
    for pid in processes:
        pid.join()

    print("Done testing all keys")
    return

if __name__ == "__main__":
    string = ""
    file = open("encrypted/5.txt", "r") # 5.txt has 588 characters

    for line in file:
        string += line.strip().replace(" ", "")
    string = string.lower()

    multiprocessing.set_start_method('spawn')

    # Run these to get find all relatively possible keys
    keys = gen_all_key_matrixes()                   # Generate all permutations of a 2x2 key
    vector_string = string_to_vec(string)           # Convert the string into sets of 2x1 vectors
    # test_all_keys(keys, vector_string)              # With single process
    test_all_keys_parallel(keys, vector_string, 4)  # With multiple processes

    # Now look through output files and find the key that worked...
    # Run these when you know the correct key
    vec_string = string_to_vec(string)
    matrix_key = np.matrix([[15,13],[9,24]])    # Correct key goes here
    print("Key used to decode message: \n", matrix_key)
    print("Decoded message:", test_key(matrix_key, vec_string)[2])