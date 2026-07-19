#!/usr/bin/env python3
"""
SSH auth log analyzer.

Parses an auth.log-style file for failed/accepted login attempts and
flags IP addresses that look like they're brute-forcing (many failures,
optionally followed by a successful login).
"""

import argparse
import re
from collections import defaultdict

FAILED_RE = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>[\d.]+)")
ACCEPTED_RE = re.compile(r"Accepted password for (?P<user>\S+) from (?P<ip>[\d.]+)")


def analyze(path: str, threshold: int = 5):
    failures = defaultdict(list)
    successes = defaultdict(list)

    with open(path) as f:
        for line in f:
            fail_match = FAILED_RE.search(line)
            if fail_match:
                failures[fail_match["ip"]].append(fail_match["user"])
                continue
            ok_match = ACCEPTED_RE.search(line)
            if ok_match:
                successes[ok_match["ip"]].append(ok_match["user"])

    suspects = {ip: users for ip, users in failures.items() if len(users) >= threshold}
    return failures, successes, suspects


def main():
    parser = argparse.ArgumentParser(description="Detect brute-force patterns in an SSH auth log.")
    parser.add_argument("logfile", nargs="?", default="sample_auth.log")
    parser.add_argument("-t", "--threshold", type=int, default=5, help="Failed attempts before flagging an IP")
    args = parser.parse_args()

    failures, successes, suspects = analyze(args.logfile, args.threshold)

    print(f"Parsed {sum(len(v) for v in failures.values())} failed and "
          f"{sum(len(v) for v in successes.values())} accepted login attempts.\n")

    if not suspects:
        print(f"No IPs exceeded {args.threshold} failed attempts.")
    else:
        print(f"Suspicious IPs (>= {args.threshold} failed attempts):")
        for ip, users in suspects.items():
            breached = " -- ALSO LOGGED IN SUCCESSFULLY" if ip in successes else ""
            print(f"  {ip}: {len(users)} failures, targeted users: {sorted(set(users))}{breached}")


if __name__ == "__main__":
    main()
