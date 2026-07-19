# SSH Auth Log Analyzer

Parses an `auth.log`-style file and flags IP addresses with excessive failed SSH login attempts - a classic brute-force detection technique used by tools like `fail2ban` and SIEM correlation rules.

## Usage

```bash
# Analyze the included sample log
python3 log_analyzer.py sample_auth.log

# Lower the threshold for flagging
python3 log_analyzer.py sample_auth.log -t 3
```

The sample log includes an IP (`203.0.113.55`) that fails 7 times against `root`/`admin` and then succeeds - a textbook brute-force-then-breach pattern - plus a second IP with only 2 failures (below the default threshold, so not flagged) and normal legitimate logins.

## What it demonstrates

- Regex-based log parsing
- Correlating events by source IP over time (the core idea behind SIEM detection rules)
- Distinguishing noisy-but-benign activity from an actual compromise pattern
