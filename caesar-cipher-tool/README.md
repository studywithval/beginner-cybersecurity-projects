# Caesar Cipher Tool

Encrypts, decrypts, and brute-forces the classical Caesar (shift) cipher.

## Usage

```bash
# Encrypt
python3 cipher_tool.py "Attack at dawn" -s 3

# Decrypt (same shift value, -d flag)
python3 cipher_tool.py "Dwwdfn dw gdzq" -s 3 -d

# Don't know the shift? Brute-force all 26 possibilities
python3 cipher_tool.py "Dwwdfn dw gdzq" -b
```

## What it demonstrates

- Classical (pre-computer) cryptography and why small keyspaces are trivially breakable by brute force
- The building-block concept (substitution) behind more modern ciphers
- A gentle intro to cryptanalysis before moving on to modern crypto (AES, RSA)
