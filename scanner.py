import socket
import json


def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)

        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"[OPEN] {host}:{port}")
            return True
        else:
            print(f"[NOT OPEN] {host}:{port}")
            return False


def save_results(host, start_port, end_port, open_ports):
    data = {
        "host": host,
        "start_port": start_port,
        "end_port": end_port,
        "open_ports": open_ports,
    }

    with open("scan_results.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Results saved to scan_results.json")


host = input("Enter target IP: ")

try:
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    if not (1 <= start_port <= end_port <= 65535):
        print("Error: Invalid port range.")

    else:
        open_ports = []

        print(f"\nStarting scan on {host}...\n")

        for port in range(start_port, end_port + 1):
            if scan_port(host, port):
                open_ports.append(port)

        print("\nScan finished")

        save_results(host, start_port, end_port, open_ports)

except ValueError:
    print("Error: Please enter a valid port number.")

except (OSError, TimeoutError) as error:
    print(f"Network error: {error}")
