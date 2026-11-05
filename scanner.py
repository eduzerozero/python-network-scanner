import socket
import json

from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)

        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"[OPEN] {host}:{port}")
            return port
        else:
            print(f"[NOT OPEN] {host}:{port}")
            return None


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


def main():
    host = input("Enter target IP: ")

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

        if not (1 <= start_port <= end_port <= 65535):
            print("Error: Invalid port range.")
            return

        try:
            socket.inet_pton(socket.AF_INET, host)

        except OSError:
            print("Error: Please enter a valid IPv4 address.")
            return

        if end_port - start_port + 1 > 1024:
            print("Error: Scan range cannot exceed 1024 ports.")

        open_ports = []

        print(f"\nStarting scan on {host}...\n")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(scan_port, host, port)
                for port in range(start_port, end_port + 1)
            ]

            for future in as_completed(futures):
                result = future.result()

                if result is not None:
                    open_ports.append(result)

        open_ports.sort()

        print("\nScan finished")

        save_results(host, start_port, end_port, open_ports)

    except ValueError:
        print("Error: Please enter a valid port number.")

    except (OSError, TimeoutError) as error:
        print(f"Network error or file error: {error}")


if __name__ == "__main__":
    main()
