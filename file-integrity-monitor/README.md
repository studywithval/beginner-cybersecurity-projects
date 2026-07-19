# File Integrity Monitor (FIM)

Saves a SHA-256 baseline of every file in a directory, then detects additions, deletions, and modifications on later runs.

## Usage

```bash
# First run: save a baseline
python3 integrity_monitor.py /path/to/watch --init

# Later: check for changes
python3 integrity_monitor.py /path/to/watch
```

## What it demonstrates

- Cryptographic hashing (SHA-256) for tamper detection
- The core mechanism behind real FIM tools (Tripwire, OSSEC, Wazuh)
- Why hash mismatches - not timestamps - are the reliable signal for detecting file tampering
