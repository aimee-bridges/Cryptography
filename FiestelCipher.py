# Lab 5 = Feistel Cipher in Python

# Permutation Function
def permutation_function(block):
    IP = [4, 0, 5, 1, 6, 2, 7, 3]
    permuted_block = (
        block[IP[0]] + block[IP[1]] + block[IP[2]] + block[IP[3]] +
        block[IP[4]] + block[IP[5]] + block[IP[6]] + block[IP[7]]
    )
    return permuted_block


# Inverse Permutation Function
def inverse_permutation_function(block):
    inverse_IP = [1, 3, 5, 7, 0, 2, 4, 6]
    inverse_permuted_block = (
        block[inverse_IP[0]] + block[inverse_IP[1]] + block[inverse_IP[2]] + block[inverse_IP[3]] +
        block[inverse_IP[4]] + block[inverse_IP[5]] + block[inverse_IP[6]] + block[inverse_IP[7]]
    )
    return inverse_permuted_block


# Switching Transformation
def switching_transformation(block):
    left = block[:4]
    right = block[4:]
    return right + left


# XOR operation
def xor(a, b):
    result = ""
    for bit_a, bit_b in zip(a, b):
        result += str(int(bit_a) ^ int(bit_b))
    return result


# Round Function g
def round_function_g(right, key):
    return xor(right, key)


# Block function Bg(x, y) = (x XOR g(y), y)
def block_function(left, right, subkey):
    g_right = round_function_g(right, subkey)
    new_left = xor(left, g_right)
    return new_left, right


# Feistel Cipher
def feistel_cipher(block, key):
    # 1. Initial permutation
    permuted_block = permutation_function(block)

    # 2. First block transformation
    left, right = permuted_block[:4], permuted_block[4:]
    left, right = block_function(left, right, key[0])
    transformed_block1 = left + right

    # 3. Switching transformation
    switched_block = switching_transformation(transformed_block1)

    # 4. Second block transformation
    left, right = switched_block[:4], switched_block[4:]
    left, right = block_function(left, right, key[1])
    transformed_block2 = left + right

    # 5. Inverse permutation
    encrypted_block = inverse_permutation_function(transformed_block2)

    return encrypted_block

#Test function
plaintext_block = "10101010"
key = ["1110", "0010"]

print(feistel_cipher(plaintext_block, key))
#Expected output: "00100011"
