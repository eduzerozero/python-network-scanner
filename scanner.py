import json
import time
import math
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(host, port, timeout):
    start = time.perf_counter()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))

        status = "OPEN"

    except ConnectionRefusedError:
        status = "CLOSED"

    except socket.timeout:
        status = "TIMEOUT"

    except OSError as error:
        status = f"ERROR: {error}"

    duration = time.perf_counter() - start

    print(f"[{status}] {host}:{port} - {duration:.3f}s")

    return {"port": port, "status": status, "duration": round(duration, 3)}


def save_results(host, start_port, end_port, timeout, scan_duration, results):
    data = {
        "host": host,
        "start_port": start_port,
        "end_port": end_port,
        "timeout": timeout,
        "scan_duration": round(scan_duration, 3),
        "results": results,
    }

    with open("scan_results.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Results saved to scan_results.json")


def main():
    host = input("Enter target IP: ")

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
        timeout = float(input("Enter timeout (seconds): "))

        if not (1 <= start_port <= end_port <= 65535):
            print("Error: Invalid port range.")
            return

        if not (math.isfinite(timeout) and 0.1 <= timeout <= 10):
            print("Error: Timeout must be between 0.1 and 10 seconds.")
            return

        try:
            socket.inet_pton(socket.AF_INET, host)
        except OSError:
            print("Error: Please enter a valid IPv4 address.")
            return

        if end_port - start_port + 1 > 1024:
            print("Error: Scan range cannot exceed 1024 ports.")
            return

        results = []

        print(f"\nStarting scan on {host}...\n")

        start_time = time.perf_counter()

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(scan_port, host, port, timeout)
                for port in range(start_port, end_port + 1)
            ]

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        results.sort(key=lambda item: item["port"])

        end_time = time.perf_counter()
        scan_duration = end_time - start_time

        print(f"\nScan completed in {scan_duration:.2f} seconds")
        print("\nScan finished.")

        save_results(host, start_port, end_port, timeout, scan_duration, results)

    except ValueError:
        print("Error: Please enter valid port numbers or timeout.")

    except (OSError, TimeoutError) as error:
        print(f"Network or file error: {error}")


if __name__ == "__main__":
    main()
