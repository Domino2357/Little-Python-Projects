import math

# sorry for my bad python! I have no clue how to deal with dual encoded numbers in this language, hence,
# this is rather laborious code


def calc_code(data, parity=0, return_as_string=True):
    # calc number of parity bits
    k = 0
    while k < math.log((len(data) + k + 1), 2):
        k += 1
    solution = []
    for char in data:
        solution.append(int(char))
    # extend code word
    all_powers = []
    for i in range(0, k):
        power = 2 ** i
        all_powers.append(power)
        solution.insert(power - 1, parity)
    # calc code word
    for power in all_powers:
        i = power - 1
        include = False
        while i < len(solution):
            comp = i + 1
            if comp % power == 0:
                include = not include
            if include and i != power - 1:
                solution[power - 1] = solution[power - 1] ^ solution[i]
            i += 1
    # return solution as a string or list
    str_sol = ''
    for bit in solution:
        str_sol = str_sol + str(bit)
    if return_as_string:
        return str_sol
    else:
        return solution


def ecc(code, parity=0):
    # indicates the index of an error
    wrong_bit = 0
    # make list out of string
    code_list = []
    for char in code:
        code_list.append(int(char))

    # calc number of parity bits
    k = math.ceil(math.log(len(code_list) + 1, 2))
    list_of_powers = []
    for j in range(0, k):
        power = 2 ** j
        list_of_powers.append(power)

    # strip away the parity bits and calculate the correct codeword for the data input
    x = get_parity_bits(code_list, list_of_powers)
    parity_bits_input = x[0]
    data_word_list = x[1]
    data_word = ''
    for bit in data_word_list:
        data_word = data_word + (str(bit))
    correct_code_word = calc_code(data_word, parity, False)
    # get the parity bits of the codeword
    parity_bits_correct = get_parity_bits(correct_code_word, list_of_powers)[0]

    # numbers of error indicating parity bits
    error_bits = []

    # compare the parity bits
    for i in range(0, len(parity_bits_input)):
        if parity_bits_correct[i] != parity_bits_input[i]:
            error_bit = 2 ** i
            error_bits.append(error_bit)
            wrong_bit += error_bit

    # return the error messages
    if wrong_bit == 0:
        return "No one-bit error here!"
    elif wrong_bit == 1:
        return "Something is fishy here, this should not happen."
    else:
        return "You have an error, at bit number: " + str(wrong_bit) + " here are the error-bits: " + str(error_bits) + "."


def get_parity_bits(data_word, list_of_powers):
    parity_bits = []
    index_offset = 0
    # parity bits are the bits at powers of two
    for power in list_of_powers:
        index = power-1
        parity_bits.append(data_word.pop(index-index_offset))
        index_offset += 1

    return [parity_bits, data_word]


if __name__ == '__main__':
    # test if calculation works
    print(calc_code('0110001010111001'))
    # test if the inverse works as well
    print(ecc(calc_code("0110101001111011", 0)))
    # test if the right error is caught
    print(ecc('111000001000111'))
