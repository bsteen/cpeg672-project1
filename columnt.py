# Converts a string into a list "key_size" columns of strings
def convert_to_columns(string, key_size):
    columns = []
    for c in range(key_size):
        columns.append("")
        for i in range(c, len(string), key_size):
            columns[c] = columns[c] + string[i]
    return columns

# Display the columns being used in row major form
# def print_columns(columns):
#     print("Showing columns:")
#     for r in columns:
#         print(r)
#     print()

if __name__ == "__main__":
    string = ""
    file = open("encrypted/3.txt", "r")

    for line in file:
        string += line.strip().replace(" ", "")
    string = string.lower()

    min_key_size = 8
    max_key_size = 10

    columns = convert_to_columns("ANDYISTHEBEST", 3)
    # print_columns(columns)