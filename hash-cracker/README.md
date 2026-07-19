# Hash Cracker (Dictionary Attack)

Cracks a password hash by hashing every word in a wordlist and comparing to the target - the same technique tools like `hashcat` and `John the Ripper` use in dictionary mode.

## Usage

```bash
# Generate a hash to test against (simulating a leaked password hash)
python3 -c "import hashlib; print(hashlib.sha256(b'dragon').hexdigest())"

# Crack it with the included sample wordlist
python3 hash_cracker.py <the-hash-from-above>

# Try a different algorithm
python3 hash_cracker.py <md5-hash> -a md5
```

## What it demonstrates

- Why unsalted fast hashes (MD5/SHA-1/SHA-256) are unsuitable for storing passwords
- Dictionary attacks vs. brute-force attacks
- Why real systems use slow, salted KDFs (bcrypt, scrypt, Argon2) instead
