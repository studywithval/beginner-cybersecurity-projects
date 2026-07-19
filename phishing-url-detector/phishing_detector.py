#!/usr/bin/env python3
"""
Heuristic phishing URL detector.

Scores a URL on common phishing indicators. This is a rule-based teaching
tool, not a replacement for real-time threat intel feeds (e.g. Google Safe
Browsing, VirusTotal) used in production.
"""

import argparse
import re
from urllib.parse import urlparse

SHORTENERS = {"bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly"}
SUSPICIOUS_KEYWORDS = {
    "login", "verify", "secure", "account", "update", "confirm",
    "banking", "signin", "webscr", "suspend",
}
IP_RE = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def analyze_url(url: str) -> dict:
    parsed = urlparse(url if "://" in url else f"http://{url}")
    host = parsed.hostname or ""
    reasons = []

    if IP_RE.match(host):
        reasons.append("Host is a raw IP address instead of a domain name")

    if host in SHORTENERS:
        reasons.append(f"Uses a URL shortener ({host})")

    if len(url) > 75:
        reasons.append("URL is unusually long")

    if "@" in url:
        reasons.append("Contains '@', which can hide the real destination")

    if not IP_RE.match(host) and host.count(".") >= 3:
        reasons.append("Unusually many subdomains")

    if parsed.scheme != "https":
        reasons.append("Not using HTTPS")

    path_and_query = f"{parsed.path} {parsed.query}".lower()
    hit_keywords = SUSPICIOUS_KEYWORDS & set(re.split(r"\W+", path_and_query))
    if hit_keywords:
        reasons.append(f"Contains sensitive-sounding keywords: {sorted(hit_keywords)}")

    if "-" in host and host not in SHORTENERS:
        reasons.append("Hyphenated domain name (common in lookalike domains)")

    score = len(reasons)
    if score == 0:
        verdict = "Likely safe"
    elif score <= 2:
        verdict = "Suspicious - review carefully"
    else:
        verdict = "High risk - likely phishing"

    return {"url": url, "score": score, "verdict": verdict, "reasons": reasons}


def main():
    parser = argparse.ArgumentParser(description="Check a URL for common phishing indicators.")
    parser.add_argument("url", help="URL to analyze")
    args = parser.parse_args()

    result = analyze_url(args.url)
    print(f"URL: {result['url']}")
    print(f"Verdict: {result['verdict']}  (risk score: {result['score']})")
    if result["reasons"]:
        print("Reasons:")
        for reason in result["reasons"]:
            print(f"  - {reason}")


if __name__ == "__main__":
    main()
