import secrets

# Generate a 32-byte key for AES-256
secure_key = secrets.token_bytes(32)
print(secure_key)