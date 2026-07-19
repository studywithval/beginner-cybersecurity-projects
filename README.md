# Beginner Cybersecurity Projects

A collection of small, self-contained security projects for building practical skills and a portfolio for entry-level security roles (SOC analyst, security engineer, junior pentester, IT security). Each project is a standalone Python script with its own README covering usage and the concepts it demonstrates.

## Projects

| Project | Skills demonstrated |
|---|---|
| [password-strength-checker](password-strength-checker/) | Input validation, entropy/scoring logic |
| [port-scanner](port-scanner/) | Sockets, TCP/IP, concurrency |
| [file-integrity-monitor](file-integrity-monitor/) | Hashing, filesystem monitoring (FIM) |
| [caesar-cipher-tool](caesar-cipher-tool/) | Classical cryptography, brute forcing |
| [log-analyzer](log-analyzer/) | Log parsing, brute-force/intrusion detection |
| [hash-cracker](hash-cracker/) | Password hashing, dictionary attacks |
| [phishing-url-detector](phishing-url-detector/) | Heuristics, social-engineering awareness |
| [packet-sniffer](packet-sniffer/) | Packet capture/analysis with Scapy |

## Getting started

```bash
git clone https://github.com/studywithval/beginner-cybersecurity-projects.git
cd beginner-cybersecurity-projects
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Each project folder has its own README with usage examples and sample data where relevant.

## Legal/ethical note

Only scan, sniff, or test systems and networks you own or have explicit written authorization to test. Several of these tools (port-scanner, packet-sniffer, hash-cracker) are dual-use; running them against systems you don't control may violate laws such as the U.S. Computer Fraud and Abuse Act or equivalent legislation elsewhere.

## Using this for job applications

- Link this repo directly on your resume/LinkedIn as a portfolio project.
- In interviews or cover letters, describe each tool in terms of the problem it solves, e.g. "Built a log analyzer that flags brute-force SSH attempts from auth logs by correlating failed logins per source IP."
- Stand out further by extending a project: add unit tests, a `--json` output mode, or a small web dashboard on top of one of these scripts.
