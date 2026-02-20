#Implementation of XOR operation for bits and bit-strings
def xor_bits(a: str, b: str) -> str:
   #XOR two single bits (0 or 1)
   if a not in ("0", "1") or b not in ("0", "1"):
       raise ValueError("Inputs must be '0' or '1'")
   return "1" if a != b else "0"

def xor_strings(s1, str, s2: str) -> str:
   #XOR two equal length bit strings
   if len(s1) != len(s2):
      raise ValueError("Bit-strings must be same length")
   return "".join(xor_bits(a, b) for a, b in zip(s1, s2))

    