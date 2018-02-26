import english_check

string = ""
file = open("encrypted/3.txt", "r")
for line in file:
    string += line.strip()
    string += " "
print(english_check.found_common_word(string))