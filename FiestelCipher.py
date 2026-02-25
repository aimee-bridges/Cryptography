#Lab 5 = Fiestel Cipher in Python

#Permutation Function
#Perform IP on 8 bit block using fixed table
def permutation_function(block: str) -> str:
    #Define IP table
    IP = [4, 0, 5, 1, 6, 2, 7, 3]
    #Build permuted block in order specificed by IP
    permuted_block = (block[IP[0]] + block[IP[1]] + block[IP[2]] + block[IP[3]] +
                      block[IP[4]] + block[IP[5]] + block[IP[6]] + block[IP[7]])
    #return permuted block
    return permuted_block 

#Inverse Permutation Function
#Perform inverse permutation
def inverse_permutation_function(block: str) -> str:
    #Define inverse IP table
    inverse_IP = [1, 3, 5, 7, 0, 2, 4, 6]
    #Build inverse permuted block
    inverse_permuted_block = (block[inverse_IP[0]] + block[inverse_IP[1]] + block[inverse_IP[2]] + block[inverse_IP[3]] +
                              block[inverse_IP[4]] + block[inverse_IP[5]] + block[inverse_IP[6]] + block[inverse_IP[7]])
    #Return inverse permuted block after IP-1
    return inverse_permuted_block

#Switching Transformation
#Swaps left and right of 8-bit block
def switching_transformation(block: str) -> str:
    #first 4 bits
    left = block[:4]
    #last 4 bits
    right = block[4:]
    #Return the block with halves swapped
    transformed_block = right + left