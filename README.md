A simple Python TCP chat with **end-to-end encryption** using `cryptography` (Fernet).

Generate a key before running:

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
