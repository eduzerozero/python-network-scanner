Python Network Scanner

A TCP port scanner developed in Python as part of my Cyber Security studies and personal learning projects.

About the Project

This project helps me develop practical skills in Python programming, TCP/IP networking, socket communication, and basic network security.

The scanner uses TCP connections to identify reachable ports on an IPv4 host.

The project is currently under active development.

Features

TCP port scanning using Python sockets

Custom IPv4 address and port range

Multithreaded scanning using ThreadPoolExecutor

Export scan results to JSON

Basic input validation and error handling

Automatic sorting of discovered open ports

Technologies

Python 3

Socket Library

JSON

Concurrent Futures

Git and GitHub

Installation

Clone the repository:

git clone https://github.com/eduzerozero/python-network-scanner.git

Navigate to the project directory:

cd python-network-scanner

Usage

Run the scanner:

python scanner.py

Example input:

Enter target IP: 127.0.0.1
Enter start port: 75
Enter end port: 85

Example output:

Starting scan on 127.0.0.1...

[NOT OPEN] 127.0.0.1:75
[NOT OPEN] 127.0.0.1:76
...
Scan finished.
Results saved to scan_results.json

JSON Export

The scanner saves results to a local JSON file.

Example:

{
    "host": "127.0.0.1",
    "start_port": 75,
    "end_port": 85,
    "open_ports": []
}

Roadmap

Basic TCP port scanning

Custom IP address and port range

Basic error handling

JSON export

Multithreaded port scanning

Scan duration measurement

Automated tests

Improved CLI arguments

Detailed scan statistics

Security Notice

This project is intended for educational purposes and authorized security testing only. Only scan systems you own or have explicit permission to test.

Author

GitHub: eduzerozero