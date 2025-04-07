def hex_to_bin(hex_string):
    hex_bin_map = {'0': "0000", '1': "0001", '2': "0010", '3': "0011",
                   '4': "0100", '5': "0101", '6': "0110", '7': "0111",
                   '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
                   'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}
    binary_string = ""
    for char in hex_string:
        binary_string += hex_bin_map[char]
    return binary_string

def bin_to_hex(bin_string):
    bin_hex_map = {"0000": '0', "0001": '1', "0010": '2', "0011": '3',
                   "0100": '4', "0101": '5', "0110": '6', "0111": '7',
                   "1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
                   "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'}
    hex_string = ""
    for i in range(0, len(bin_string), 4):
        chunk = bin_string[i:i+4]
        hex_string += bin_hex_map[chunk]
    return hex_string

def bin_to_dec(bin_number):
    decimal_number = 0
    bin_number_str = str(bin_number)
    for i, digit in enumerate(bin_number_str[::-1]):
        decimal_number += int(digit) * (2 ** i)
    return decimal_number

def dec_to_bin(decimal_number):
    binary_string = bin(decimal_number).replace("0b", "")
    while len(binary_string) % 4 != 0:
        binary_string = '0' + binary_string
    return binary_string

def permute(input_string, permutation_table, n):
    permuted_string = ""
    for i in range(n):
        permuted_string += input_string[permutation_table[i] - 1]
    return permuted_string

def shift_left(key_chunk, shifts):
    shifted_key = key_chunk[shifts:] + key_chunk[:shifts]
    return shifted_key

def xor_strings(string1, string2):
    xor_result = ""
    for i in range(len(string1)):
        xor_result += '0' if string1[i] == string2[i] else '1'
    return xor_result

initial_permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                       60, 52, 44, 36, 28, 20, 12, 4,
                       62, 54, 46, 38, 30, 22, 14, 6,
                       64, 56, 48, 40, 32, 24, 16, 8,
                       57, 49, 41, 33, 25, 17, 9, 1,
                       59, 51, 43, 35, 27, 19, 11, 3,
                       61, 53, 45, 37, 29, 21, 13, 5,
                       63, 55, 47, 39, 31, 23, 15, 7]

expansion_d_box = [32, 1, 2, 3, 4, 5, 4, 5,
                   6, 7, 8, 9, 8, 9, 10, 11,
                   12, 13, 12, 13, 14, 15, 16, 17,
                   16, 17, 18, 19, 20, 21, 20, 21,
                   22, 23, 24, 25, 24, 25, 26, 27,
                   28, 29, 28, 29, 30, 31, 32, 1]

straight_permutation = [16, 7, 20, 21,
                        29, 12, 28, 17,
                        1, 15, 23, 26,
                        5, 18, 31, 10,
                        2, 8, 24, 14,
                        32, 27, 3, 9,
                        19, 13, 30, 6,
                        22, 11, 4, 25]

sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

final_permutation = [40, 8, 48, 16, 56, 24, 64, 32,
                     39, 7, 47, 15, 55, 23, 63, 31,
                     38, 6, 46, 14, 54, 22, 62, 30,
                     37, 5, 45, 13, 53, 21, 61, 29,
                     36, 4, 44, 12, 52, 20, 60, 28,
                     35, 3, 43, 11, 51, 19, 59, 27,
                     34, 2, 42, 10, 50, 18, 58, 26,
                     33, 1, 41, 9, 49, 17, 57, 25]

def encrypt(plain_text, round_keys_bin, round_keys_hex):
    plain_text_bin = hex_to_bin(plain_text)
    permuted_text = permute(plain_text_bin, initial_permutation, 64)
    print("After initial permutation", bin_to_hex(permuted_text))

    left_half = permuted_text[:32]
    right_half = permuted_text[32:]

    for i in range(16):
        expanded_right = permute(right_half, expansion_d_box, 48)
        xor_result = xor_strings(expanded_right, round_keys_bin[i])

        sbox_output = ""
        for j in range(8):
            row = bin_to_dec(int(xor_result[j * 6] + xor_result[j * 6 + 5]))
            col = bin_to_dec(int(xor_result[j * 6 + 1:j * 6 + 5]))
            sbox_value = sbox[j][row][col]
            sbox_output += dec_to_bin(sbox_value)

        sbox_permuted = permute(sbox_output, straight_permutation, 32)
        result = xor_strings(left_half, sbox_permuted)
        left_half = result

        if i != 15:
            left_half, right_half = right_half, left_half

        print("Round ", i + 1, " ", bin_to_hex(left_half), " ", bin_to_hex(right_half), " ", round_keys_hex[i])

    combined_text = left_half + right_half
    cipher_text = permute(combined_text, final_permutation, 64)
    return cipher_text

plain_text = "Adityabandaru123"
key = "1234567812345678"

key_bin = hex_to_bin(key)
key_permuted = permute(key_bin, [57, 49, 41, 33, 25, 17, 9,
                                 1, 58, 50, 42, 34, 26, 18,
                                 10, 2, 59, 51, 43, 35, 27,
                                 19, 11, 3, 60, 52, 44, 36,
                                 63, 55, 47, 39, 31, 23, 15,
                                 7, 62, 54, 46, 38, 30, 22,
                                 14, 6, 61, 53, 45, 37, 29,
                                 21, 13, 5, 28, 20, 12, 4], 56)

left_key = key_permuted[:28]
right_key = key_permuted[28:]

round_keys_bin = []
round_keys_hex = []
for i in range(16):
    left_key = shift_left(left_key, [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1][i])
    right_key = shift_left(right_key, [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1][i])
    combined_key = left_key + right_key
    round_key = permute(combined_key, [14, 17, 11, 24, 1, 5, 3, 28,
                                       15, 6, 21, 10, 23, 19, 12, 4,
                                       26, 8, 16, 7, 27, 20, 13, 2,
                                       41, 52, 31, 37, 47, 55, 30, 40,
                                       51, 45, 33, 48, 44, 49, 39, 56,
                                       34, 53, 46, 42, 50, 36, 29, 32], 48)
    round_keys_bin.append(round_key)
    round_keys_hex.append(bin_to_hex(round_key))

print("Encryption")
cipher_text = bin_to_hex(encrypt(plain_text, round_keys_bin, round_keys_hex))
print("Cipher Text : ", cipher_text)

print("Decryption")
round_keys_bin.reverse()
round_keys_hex.reverse()
decrypted_text = bin_to_hex(encrypt(cipher_text, round_keys_bin, round_keys_hex))
print("Plain Text : ", decrypted_text)