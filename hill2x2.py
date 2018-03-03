import itertools
import numpy as np
import threading
import time
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
def test_key(matrix_key, vector_string, thread_id):
    decoded = ""

    # Perform the matrix multiplication and convert the result back to characters
    for vec in vector_string:
        vec_result = (matrix_key * vec) % 26
        decoded += ntc(vec_result[0][0]) + ntc(vec_result[1][0])

    # Check if the decoded string in plain text English
    sqr_eng_sum = english_check.squared_eng_freq(decoded)
    if abs(sqr_eng_sum - 0.065) < 0.005:
        return True, sqr_eng_sum, decoded
    else:
        return False, sqr_eng_sum, decoded

# Given a list of key matrixes and an input string in the form of a list of 2x1
# vectors, test all the keys on the input string
# def test_all_keys(keys, vector_string):
#     print("Testing all keys...")
#     count = 1

#     for key in keys:
#         test_key(key, vector_string, 0)
#         if count % 1000 == 0:
#             print("Number of keys tested:", count, "\n")
#         count += 1

#     print("Done testing all keys")
#     return

# Worker function for a thread; Used by test_all_keys_threaded
def thread_worker(key_set, vector_string, start, end, thread_id):
    print("Starting thread:", thread_id, "Range:", start, end - 1)
    output_file = open("output/out_" + str(thread_id), "w")
    output_file.writelines("Thread: " + str(thread_id) + "\nRange: " + str(start) + " " + str(end - 1) + "\n\n")
    time.sleep(0.2)

    count = 0
    for key in key_set:
        text_check, sqr_eng_sum, decoded = test_key(key, vector_string, thread_id)
        if text_check:
            output_file.writelines("Tested key:\n"+ str(key) + "\nSquared English sum:" + str(sqr_eng_sum) + "\nDecoded text: " + decoded[:42] + "\n\n")

        count += 1
        if count % 1000 == 0:
            print("Thread " + str(thread_id) + " at " + str(count) + " of " + str(end - start))

    output_file.close()
    print("Thread", thread_id, "finished range:", start, end)
    return

# Same as test_all_keys, except does it will multiple threads
def test_all_keys_threaded(keys, vector_string, num_threads):
    print("Testing all keys with", num_threads, "threads...")
    num_keys = len(keys)
    threads = []

    for thread_id in range(num_threads):
        start_idx = (num_keys // num_threads) * thread_id
        end_idx = (num_keys // num_threads) * thread_id + (num_keys // num_threads)
        new_thread = threading.Thread(target = thread_worker, args = (keys[start_idx:end_idx], vector_string, start_idx, end_idx, thread_id))
        threads.append(new_thread)
        new_thread.start()

    # Main thread blocks until all threads are finished
    for thread in threads:
        thread.join()

    print("Done testing all keys")
    return

if __name__ == "__main__":
    string = ""
    file = open("encrypted/5.txt", "r")
    # 5.txt has 588 characters

    for line in file:
        string += line.strip().replace(" ", "")

    keys = gen_all_key_matrixes()
    vector_string = string_to_vec(string)
    test_all_keys_threaded(keys, vector_string, 12)     # Multithread brute force

    # vec_string = string_to_vec("plhzaoplzp")
    # matrix_key = np.matrix([[1,2],[3,4]])
    # test_key(matrix_key, vec_string)