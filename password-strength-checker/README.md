# Password Strength Checker

Scores a password against common strength criteria (length, character variety, repetition, membership in a list of commonly leaked passwords) and estimates its entropy in bits.

## Usage

```bash
python3 password_checker.py "Tr0ub4dor&3"
# or omit the argument to be prompted with hidden input:
python3 password_checker.py
```

## What it demonstrates

- Why length matters more than complexity past a point (entropy calculation)
- Common password blocklisting, the same idea used by real auth systems (e.g. NIST SP 800-63B guidance against known-breached passwords)
- Basic regex-based input analysis
