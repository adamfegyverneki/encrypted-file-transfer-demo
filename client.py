import socket
import hashlib
from cryptography.fernet import Fernet

def calculate_sha256(file_path):
    """Calculate SHA-256 checksum of a file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha.update(chunk)
    return sha.hexdigest()

def send_file(host, port, key, file_path):
    fernet = Fernet(key)
    with open(file_path, "rb") as f:
        plaintext = f.read()
    encrypted = fernet.encrypt(plaintext)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(encrypted)

    checksum = calculate_sha256(file_path)
    print("[+] File sent securely.")
    print(f"[+] SHA-256: {checksum}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python client.py <host> <port> <file> <key>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    key = sys.argv[4].encode()  # fernet key must be shared before
    send_file(host, port, key, file_path)
