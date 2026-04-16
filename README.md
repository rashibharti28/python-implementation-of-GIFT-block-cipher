#  GIFT-64 Block Cipher (Python Implementation)

This repository contains a **from-scratch Python implementation** of the **GIFT-64 lightweight block cipher** with a 128-bit key.
It includes detailed round-by-round debugging output and verification using standard test vectors.

---

##  Overview

**GIFT-64** is a lightweight block cipher designed for:

* Low-area hardware implementations
* IoT and embedded systems
* Energy-efficient cryptography

###  Specifications

* **Block size:** 64 bits
* **Key size:** 128 bits
* **Number of rounds:** 28
* **Structure:** Substitution-Permutation Network (SPN)



##  Algorithm Structure

Each round of GIFT-64 consists of:

1. **SubCells (S-box layer)**
2. **PermBits (bit permutation layer)**
3. **AddRoundKey (key mixing)**
4. **AddRoundConstant**

---

##  Test Vectors

The implementation is verified using standard test vectors



## ▶ Usage

### 🔹 Run Encryption Test

```bash
python main.py
```

###  Sample Output

```
 GIFT-64 ENCRYPTION TEST 

Plaintext : 0x0
Expected  : 0xf62bc3ef34f775ac
Got       : 0xf62bc3ef34f775ac
 PASS

Plaintext : 0xfedcba9876543210
Expected  : 0xc1b71f66160ff587
Got       : 0xc1b71f66160ff587
 PASS
```

---

##  Project Structure

```
            
├── gift64.py           # Core cipher implementation
├── test_vectors.py     # Test cases
└── README.md
```

---

## Debugging Support

The implementation prints intermediate values for each round:

* Before round
* After S-box
* After permutation
* After key addition

This helps in:

* Understanding cipher internals
* Debugging incorrect implementations
* Verifying against reference traces

---

## 🚨 Common Pitfalls

If test cases fail:

-  Incorrect key schedule
-  Missing round constants
- Wrong bit permutation
-  Applying full key instead of partial key

---

##  Learning Outcomes

By working with this project, you will understand:

* Lightweight cryptography design
* SPN-based cipher structure
* Bit-level permutation logic
* Key scheduling techniques

---




##  References




