# 1
def three_x_cubed_plus_5(x):
    return 3*x*x*x+5
print(three_x_cubed_plus_5(2))
print(three_x_cubed_plus_5(2345678))
print(three_x_cubed_plus_5(-20))



# 2
def mystery_code(s, i):
    alphabet = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    result = ""
    for c in s:
        if (not c.isalpha()) or c.isdigit():
            temp = c
        elif c.isupper():
            temp = c.lower()
            ind = alphabet.index(temp)
            ind = ind + i
            if ind > 26:
                ind = ind % 26
            temp = alphabet[ind]
        elif c.islower():
            ind = alphabet.index(c)
            ind = ind + i
            if ind > 26:
                ind = ind % 26
            temp = alphabet[ind]
            temp = temp.upper()
        result = result + temp
    return result

print(mystery_code("abc Iz th1s Secure? n0, no, 9!", 17))
print(mystery_code("abc Iz th1s Secure? n0, no, 9!", 12413424))
print(mystery_code("abc Iz th1s Secure? n0, no, 9!", 0))


# 3
def quadruples(xlist):
    final_list = []
    temp_list = []
    count = 0
    for x in xlist:
        temp_list.append(x)
        count = count + 1
        if count == 4:
            final_list.append(temp_list)
            count = 0
            temp_list = []
    if count > 0:
        final_list.append(temp_list)
    return final_list

print(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1]))
print(quadruples([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 5, 6, 7, 88, 13, 54, 44]))
print(quadruples([]))


# 4
def past_tense(word_list):
    vowel_list = ['a', 'e', 'i', 'o', 'u']
    special_list = {'eat': 'ate', 'have': 'had', 'go': 'went', 'be': 'was'}
    final_list = []
    for word in word_list:
        if word in special_list.keys():
            temp = special_list[word]
        else:
            w = list(word)
            length = len(word)
            if w[length - 1] == 'e':
                w.append('d')
                temp = "".join(w)
            elif w[length - 1] == 'y' and (not w[length - 2] in vowel_list):
                w[length - 1] = 'i'
                temp = "".join(w) + 'ed'
            elif (not w[length - 1] in vowel_list) and (w[length - 2] in vowel_list) and (not w[length - 3] in vowel_list):
                w.append(w[length - 1])
                temp = "".join(w) + 'ed'
            else:
                temp = word + 'ed'
        final_list.append(temp)
    return final_list

print(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat', 'try', 'go']))
print(past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat', 'try', 'go', 'fry', 'destroy', 'enjoy']))
print(past_tense([]))

