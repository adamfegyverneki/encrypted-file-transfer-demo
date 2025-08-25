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

def run_server(host, port, key, save_as="received_file.txt"):
    fernet = Fernet(key)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.bind((host, port))
        srv.listen(1)
        print(f"[+] Server listening on {host}:{port}")
        
        conn, addr = srv.accept()
        with conn:
            print(f"[+] Connection from {addr}")
            encrypted_data = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                encrypted_data += data

            decrypted_data = fernet.decrypt(encrypted_data)
            with open(save_as, "wb") as f:
                f.write(decrypted_data)

            checksum = calculate_sha256(save_as)
            print(f"[+] File saved as {save_as}")
            print(f"[+] SHA-256: {checksum}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python server.py <port> <key>")
        sys.exit(1)

    port = int(sys.argv[1])
    key = sys.argv[2].encode()  # fernet key must be shared before
    run_server("localhost", port, key)
