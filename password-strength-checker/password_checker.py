#!/usr/bin/env python3
"""Password Strength Checker - scores a password and explains how to improve it."""

import argparse
import math
import re

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "abc123", "password1", "111111", "123123", "letmein", "iloveyou",
    "admin", "welcome", "monkey", "dragon", "football", "baseball",
}


def score_password(password: str) -> dict:
    length = len(password)
    checks = {
        "length_ok": length >= 12,
        "has_lower": bool(re.search(r"[a-z]", password)),
        "has_upper": bool(re.search(r"[A-Z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_symbol": bool(re.search(r"[^\w\s]", password)),
        "not_common": password.lower() not in COMMON_PASSWORDS,
        "no_repeats": not re.search(r"(.)\1{2,}", password),
    }

    charset = 0
    if checks["has_lower"]:
        charset += 26
    if checks["has_upper"]:
        charset += 26
    if checks["has_digit"]:
        charset += 10
    if checks["has_symbol"]:
        charset += 32
    entropy = length * math.log2(charset) if charset else 0

    score = sum(checks.values())
    if not checks["not_common"]:
        score = 0

    if score >= 6:
        rating = "Strong"
    elif score >= 4:
        rating = "Moderate"
    else:
        rating = "Weak"

    return {"checks": checks, "entropy_bits": round(entropy, 1), "score": score, "rating": rating}


def main():
    parser = argparse.ArgumentParser(description="Check the strength of a password.")
    parser.add_argument("password", nargs="?", help="Password to check (omit to be prompted, hidden input)")
    args = parser.parse_args()

    password = args.password
    if not password:
        import getpass
        password = getpass.getpass("Enter password to check: ")

    result = score_password(password)

    print(f"\nRating: {result['rating']}  (score {result['score']}/7, ~{result['entropy_bits']} bits entropy)")
    print("\nChecklist:")
    labels = {
        "length_ok": "At least 12 characters",
        "has_lower": "Contains lowercase letters",
        "has_upper": "Contains uppercase letters",
        "has_digit": "Contains digits",
        "has_symbol": "Contains symbols",
        "not_common": "Not a commonly leaked password",
        "no_repeats": "No 3+ repeated characters in a row",
    }
    for key, label in labels.items():
        mark = "OK " if result["checks"][key] else "X  "
        print(f"  {mark} {label}")


if __name__ == "__main__":
    main()
