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

#TASK 2: Permutation Testing
#how changing the permutation (IP and IP-1) affect output

def test_permutation_variation(block, key, IP, inverse_IP):
    
    #Apply a custom IP and IP-1, run a 2-round Feistel encryption using block_function & switching_transformation.
    
    #1. Apply custom initial permutation (IP)
    permuted = "".join(block[i] for i in IP)

    # 2. First block transformation using key[0]
    left, right = permuted[:4], permuted[4:]
    left, right = block_function(left, right, key[0])
    block1 = left + right

    # 3. Switching transformation (SW)
    switched = switching_transformation(block1)

    # 4. Second block transformation using key[1]
    left, right = switched[:4], switched[4:]
    left, right = block_function(left, right, key[1])
    block2 = left + right

    # 5. Apply custom inverse permutation (IP-1)
    encrypted = "".join(block2[i] for i in inverse_IP)

    # 6. Return the resulting ciphertext
    return encrypted


#TASK 2 Example
# Define a new permutation and its inverse
task2_IP = [2, 4, 6, 0, 1, 3, 5, 7]
task2_inverse_IP = [3, 4, 0, 5, 1, 6, 2, 7]

plaintext_block = "10101010"
key = ["1110", "0010"]

print("TASK 2 - Permutation Test:")
print("Plaintext:", plaintext_block)
print("Ciphertext with custom IP:", test_permutation_variation(plaintext_block, key, task2_IP, task2_inverse_IP))

#TASK 3: Block Transformation
#how changing keys and the round functionaffects the ciphertext


#3A – Key variation using the existing Feistel cipher
def test_key_variation(block, key):
    """
    Use different round keys with the existing feistel_cipher
    to see how the ciphertext changes.
    """
    return feistel_cipher(block, key)


# ----- TASK 3A Example -----
plaintext_block = "10101010"
key_variant = ["0000", "1111"]

print("\nTASK 3A - Key Variation Test:")
print("Plaintext:", plaintext_block)
print("Keys:", key_variant)
print("Ciphertext:", test_key_variation(plaintext_block, key_variant))


# 3B – Round function variation
def test_round_function(block, key, custom_round_function):
    """
    Use a custom round function g instead of the default round_function_g
    while keeping the Feistel structure the same.
    """

    # Local block function that uses the custom round function
    def custom_block(left, right, subkey):
        g_right = custom_round_function(right, subkey)
        new_left = xor(left, g_right)
        return new_left, right

    #1. Initial permutation
    permuted = permutation_function(block)

    #2. First round with custom g
    left, right = permuted[:4], permuted[4:]
    left, right = custom_block(left, right, key[0])
    block1 = left + right

    #3. Switching transformation
    switched = switching_transformation(block1)

    #4. Second round with custom g
    left, right = switched[:4], switched[4:]
    left, right = custom_block(left, right, key[1])
    block2 = left + right

    #5. Inverse permutation
    encrypted = inverse_permutation_function(block2)

    return encrypted


#Example custom round functions for experimentation

def rotate_right(right, subkey):
    """
    Custom round function:
    Rotate the 4-bit right half by 1 bit to the right.
    Ignores the subkey (for demonstration).
    """
    return right[-1] + right[:-1]


def invert_bits(right, subkey):
    """
    Custom round function:
    Invert each bit in the right half (0 -> 1, 1 -> 0).
    Ignores the subkey (for demonstration).
    """
    return "".join("1" if b == "0" else "0" for b in right)


# ----- TASK 3B Examples -----
plaintext_block = "10101010"
key = ["1110", "0010"]

print("\nTASK 3B - Round Function Variation (Rotate Right):")
print("Plaintext:", plaintext_block)
print("Ciphertext:", test_round_function(plaintext_block, key, rotate_right))

print("\nTASK 3B - Round Function Variation (Invert Bits):")
print("Plaintext:", plaintext_block)
print("Ciphertext:", test_round_function(plaintext_block, key, invert_bits))