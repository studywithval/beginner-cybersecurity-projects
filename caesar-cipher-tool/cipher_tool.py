#!/usr/bin/env python3
"""Classic Caesar cipher: encrypt, decrypt, and brute-force all shifts."""

import argparse

ALPHABET_SIZE = 26


def shift_char(ch: str, shift: int) -> str:
    if ch.isupper():
        return chr((ord(ch) - ord("A") + shift) % ALPHABET_SIZE + ord("A"))
    if ch.islower():
        return chr((ord(ch) - ord("a") + shift) % ALPHABET_SIZE + ord("a"))
    return ch


def caesar(text: str, shift: int) -> str:
    return "".join(shift_char(ch, shift) for ch in text)


def brute_force(text: str):
    for shift in range(ALPHABET_SIZE):
        print(f"  shift {shift:>2}: {caesar(text, shift)}")


def main():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt text with a Caesar cipher.")
    parser.add_argument("text", help="Text to process")
    parser.add_argument("-s", "--shift", type=int, help="Shift amount (positive = encrypt)")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt using --shift instead of encrypting")
    parser.add_argument("-b", "--brute-force", action="store_true", help="Try all 26 shifts (for cracking ciphertext)")
    args = parser.parse_args()

    if args.brute_force:
        print("Trying all shifts:")
        brute_force(args.text)
        return

    if args.shift is None:
        parser.error("--shift is required unless --brute-force is used")

    shift = -args.shift if args.decrypt else args.shift
    print(caesar(args.text, shift))


if __name__ == "__main__":
    main()
