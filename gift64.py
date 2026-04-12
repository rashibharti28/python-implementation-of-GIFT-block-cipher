
# GIFT-64 Implementation 
from test_vectors import TEST_VECTORS

#S-BOX 
SBOX = [1,10,4,12,6,15,3,9,2,13,11,7,5,0,8,14]

def sbox_layer(state):
    new_state = 0
    for i in range(16):
        nibble = (state >> (4*i)) & 0xF
        new_state |= SBOX[nibble] << (4*i)
    return new_state


# PERMUTATION Layer
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
    U = (key >> 16) & 0xFFFF
    V = key & 0xFFFF

    # key addition
    for i in range(16):
        if (U >> i) & 1:
            state ^= (1 << (4*i + 1))
        if (V >> i) & 1:
            state ^= (1 << (4*i))

    # round constants
    positions = [3,7,11,15,19,23]
    for i in range(6):
        if (rc >> i) & 1:
            state ^= (1 << positions[i])

    # fixed bit
    state ^= (1 << 63)

    return state


# one round function
def round_function(state, key, rc, debug=False):
    if debug:
        print("Before      :", hex(state))

    state = sbox_layer(state)
    if debug:
        print("After SBOX  :", hex(state))

    state = permute_bits(state)
    if debug:
        print("After Perm  :", hex(state))

    state = add_round_key(state, key, rc)
    if debug:
        print("After Key   :", hex(state))

    return state


#key schedule
def split_key(key):
    return [(key >> (16*i)) & 0xFFFF for i in range(8)]

def update_key(key_words):
    # rotate words
    new_key = key_words[1:] + key_words[:1]

    # rotate bits inside words
    k6 = new_key[6]
    k7 = new_key[7]

    new_key[6] = ((k7 >> 2) | (k7 << 14)) & 0xFFFF
    new_key[7] = ((k6 >> 12) | (k6 << 4)) & 0xFFFF

    return new_key

def get_round_key(key_words):
    U = key_words[1]
    V = key_words[0]
    return (U << 16) | V


# Round constant

GIFT_RC = [
0x01,0x03,0x07,0x0F,0x1F,0x3E,0x3D,0x3B,
0x37,0x2F,0x1E,0x3C,0x39,0x33,0x27,0x0E,
0x1D,0x3A,0x35,0x2B,0x16,0x2C,0x18,0x30,
0x21,0x02,0x05,0x0B
]


# full encryption
def gift64_encrypt(state, master_key, debug=False):
    key_words = split_key(master_key)

    for r in range(28):
        if debug:
            print(f"\n=== ROUND {r} ===")

        round_key = get_round_key(key_words)
        rc = GIFT_RC[r]

        state = round_function(state, round_key, rc, debug)

        key_words = update_key(key_words)

    return state


# test
if __name__ == "__main__":

    print("=== GIFT-64 ENCRYPTION TEST ===")

   

for test in TEST_VECTORS:
    pt = test["plaintext"]
    key = test["key"]
    expected = test["ciphertext"]

    result = gift64_encrypt(pt, key,debug=True)

    print("Plaintext :", hex(pt))
    print("Expected  :", hex(expected))
    print("Got       :", hex(result))

    if result == expected:
        print("✅ PASS\n")
    else:
        print("❌ FAIL\n")    