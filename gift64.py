# GIFT-64 Implementation 
from test_vectors import TEST_VECTORS

# S-BOX 
SBOX = [1,10,4,12,6,15,3,9,2,13,11,7,5,0,8,14]

def sbox_layer(state):
    new_state = 0
    for i in range(16):
        nibble = (state >> (4*i)) & 0xF
        new_state |= SBOX[nibble] << (4*i)
    return new_state


# permutation Layer
PBOX = [
0,17,34,51,48,1,18,35,32,49,2,19,16,33,50,3,
4,21,38,55,52,5,22,39,36,53,6,23,20,37,54,7,
8,25,42,59,56,9,26,43,40,57,10,27,24,41,58,11,
12,29,46,63,60,13,30,47,44,61,14,31,28,45,62,15
]

def permute_bits(state):
    new_state = 0
    for i in range(64):
        bit = (state >> i) & 1
        new_state |= bit << PBOX[i]
    return new_state


# Add Round Key 
def add_round_key(state, key, rc):

    # key is 128-bit → convert to bit list
    key_bits = [(key >> i) & 1 for i in range(128)]

    # Apply key bits exactly like reference
    kbc = 0
    for i in range(16):
        # bit positions
        if key_bits[kbc]:
            state ^= (1 << (4*i))
        if key_bits[kbc + 16]:
            state ^= (1 << (4*i + 1))
        kbc += 1

    # round constants
    RC_POS = [3,7,11,15,19,23]
    for i in range(6):
        if (rc >> i) & 1:
            state ^= (1 << RC_POS[i])

    # fixed bit
    state ^= (1 << 63)

    return state


# one round function
def round_function(state, round_key, rc, debug=False):
    if debug:
        print("Before      :", hex(state))

    state = sbox_layer(state)
    if debug:
        print("After SBOX  :", hex(state))

    state = permute_bits(state)
    if debug:
        print("After Perm  :", hex(state))

    state = add_round_key(state, round_key, rc)
    if debug:
        print("After Key   :", hex(state))

    return state



# KEY SCHEDULE 


def update_key(key):
    # convert key into 32 nibbles (like reference)
    K = [(key >> (4*i)) & 0xF for i in range(32)]

    temp = [0]*32

    # rotate entire key (>>32 bits → 8 nibbles)
    for i in range(32):
        temp[i] = K[(i+8) % 32]

    # update first 24 nibbles
    for i in range(24):
        K[i] = temp[i]

    # k0 >> 12 (nibble rotation)
    K[24] = temp[27]
    K[25] = temp[24]
    K[26] = temp[25]
    K[27] = temp[26]

    # k1 >> 2 (bit-level rotation inside nibble)
    K[28] = ((temp[28] & 0xC) >> 2) | ((temp[29] & 0x3) << 2)
    K[29] = ((temp[29] & 0xC) >> 2) | ((temp[30] & 0x3) << 2)
    K[30] = ((temp[30] & 0xC) >> 2) | ((temp[31] & 0x3) << 2)
    K[31] = ((temp[31] & 0xC) >> 2) | ((temp[28] & 0x3) << 2)

    # rebuild 128-bit key
    new_key = 0
    for i in range(32):
        new_key |= K[i] << (4*i)

    return new_key


# Round constant
GIFT_RC = [
0x01,0x03,0x07,0x0F,0x1F,0x3E,0x3D,0x3B,
0x37,0x2F,0x1E,0x3C,0x39,0x33,0x27,0x0E,
0x1D,0x3A,0x35,0x2B,0x16,0x2C,0x18,0x30,
0x21,0x02,0x05,0x0B
]


# full encryption
def gift64_encrypt(state, master_key, debug=False):

    key = master_key  # 128-bit key

    for r in range(28):
        if debug:
            print(f"\n ROUND {r}")

        rc = GIFT_RC[r]

        state = round_function(state, key, rc, debug)

        key = update_key(key)

    return state


# test
if __name__ == "__main__":

    print("GIFT-64 ENCRYPTION TEST")

    for test in TEST_VECTORS:
        pt = test["plaintext"]
        key = test["key"]
        expected = test["ciphertext"]

        result = gift64_encrypt(pt, key, debug=True)

        print("Plaintext :", hex(pt))
        print("Expected  :", hex(expected))
        print("Got       :", hex(result))

        if result == expected:
            print(" PASS\n")
        else:
            print(" FAIL\n")