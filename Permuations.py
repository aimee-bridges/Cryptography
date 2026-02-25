def appl_permutation(bits: str, perm: list[int]) -> str:
    #Apply permutation to a bit-string
    #perm is a list of 1 based indices

    if len(bits) != len(perm):
        raise ValueError("Permutation length must match bit-string length")
    #Build permuted string by selecting bits in order of perm
    return "".join(bits[i-1] for i in perm)

#Predefined permutations from Lecture 4
IP = [5, 1, 6, 2, 7, 3, 8, 4]
IP_INV = [2, 4, 6, 8, 1, 3, 5, 7]
