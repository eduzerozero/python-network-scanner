import socket

host = input("Enter target IP: ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))


def scan_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)

        result = sock.connect_ex((host, port))

        if result == 0:
            print(f"[OPEN] {host}:{port}")
        else:
            print(f"[NOT OPEN] {host}:{port}")


print(f"\nStarting scan on {host}...\n")


for port in range(start_port, end_port + 1):
    scan_port(host, port)

print("\nScan finished.")
