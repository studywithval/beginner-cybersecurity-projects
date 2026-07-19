#!/usr/bin/env python3
"""
Dictionary-based hash cracker.

Demonstrates why weak/common passwords are crackable in seconds and why
salting plus slow hashing (bcrypt/scrypt/argon2) matters. Only use against
hashes you own or are authorized to test.
"""

import argparse
import hashlib

ALGOS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
}


def crack(target_hash: str, wordlist_path: str, algo: str = "sha256"):
    hasher = ALGOS[algo]
    target_hash = target_hash.lower()

    with open(wordlist_path, encoding="utf-8", errors="ignore") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            if hasher(word.encode()).hexdigest() == target_hash:
                return word
    return None


def main():
    parser = argparse.ArgumentParser(description="Crack a hash using a wordlist (dictionary attack).")
    parser.add_argument("hash", help="Target hash to crack")
    parser.add_argument("-w", "--wordlist", default="sample_wordlist.txt", help="Path to wordlist")
    parser.add_argument("-a", "--algo", choices=list(ALGOS), default="sha256", help="Hash algorithm")
    args = parser.parse_args()

    print(f"Trying {args.algo} dictionary attack against: {args.hash}")
    result = crack(args.hash, args.wordlist, args.algo)

    if result:
        print(f"\nCracked! Password is: {result}")
    else:
        print("\nNo match found in wordlist.")


if __name__ == "__main__":
    main()
