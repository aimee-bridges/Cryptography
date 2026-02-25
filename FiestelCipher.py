#Lab 5 = Fiestel Cipher in Python

#Permutation Function
#Perform IP on 8 bit block using fixed table
def permutation_function(block):
    #Define IP table
    IP = [4, 0, 5, 1, 6, 2, 7, 3]
    #Build permuted block in order specificed by IP
    permuted_block = (block[IP[0]] + block[IP[1]] + block[IP[2]] + block[IP[3]] +
                      block[IP[4]] + block[IP[5]] + block[IP[6]] + block[IP[7]])
    #return permuted block
    return permuted_block 

#Inverse Permutation Function
#Perform inverse permutation
def inverse_permutation_function(block):
    #Define inverse IP table
    inverse_IP = [1, 3, 5, 7, 0, 2, 4, 6]
    #Build inverse permuted block
    inverse_permuted_block = (block[inverse_IP[0]] + block[inverse_IP[1]] + block[inverse_IP[2]] + block[inverse_IP[3]] +
                              block[inverse_IP[4]] + block[inverse_IP[5]] + block[inverse_IP[6]] + block[inverse_IP[7]])
    #Return inverse permuted block after IP-1
    return inverse_permuted_block

#Switching Transformation
#Swaps left and right of 8-bit block
def switching_transformation(block):
    #transformed block
    transformed_block = block[1] + block[0]
    #return block
    return transformed_block

#XOR operation
def xor(a, b):
    #empty string for XOR results for each bit
    result = ""
    # Iteration of bits of input strings
    for bit_a, bit_b in zip(a, b):
        #convert bits to integers, apply bitwise XOR
        #convert the result back to string and append to result
        result += str(int(bit_a) ^ int(bit_b))
    #return the resulting bit-string
    return result

#Round Function
#Fiestel round by XOR on right half with subkey
def round_function_g (right, key):
    #apply XOR between right half and round subkey
    return xor (right, key)

#Block function
#Bg(x,y) = (y, x XOR g(y, key)) per Fiestel round
def block_function(left, right, subkey):
    #g_right using round function and subkey
    g_right = round_function_g (right, subkey)
    #return updated left half
    return xor(left, g_right), right

#Fiestel Cipher
def feistel_cipher(block, key):
    #1 Permutation IP
    permuted_block = permutation_function(block)
    #2 Block transformation with first subkey
    left, right = permuted_block[:4], permuted_block[4:]
    transformed_block1 = block_function(left, right, key[0])
    #3 Switching transformation
    switched_block = switching_transformation (transformed_block1)
    #4 Block transformation with second subkey
    left, right = switched_block[:4], switched_block[4:]
    transformed_block2 = block_function(left, right, key[1])
    #5 Inverse Permutation IP-1
    transformed_block2 = transformed_block2[0] + transformed_block2[1]
    encrypted_block = inverse_permutation_function(transformed_block2)
    #return encrypted block
    return encrypted_block
