# ARRH – AES-256-GCM DECRYPTOR 

A Python-based file That Decryption utility that uses AES-256-GCM for Decrpyting & Encrpyting Hidden Tokens & Important Files Saved by someone you know they will try to hide it from you :) 

---

## Features

* AES-256-GCM authenticated encryption
* Creates `.backup` files before encryption
* Cross-platform support for Windows, macOS, and Linux
* PBKDF2-SHA256 key derivation

---

## Requirements

* Python 3.8 or higher
* `cryptography` library

---

## Installation

Install the required dependency:

### Windows

```cmd
pip install cryptography
```

### macOS / Linux

```bash
pip3 install cryptography
```

---

# Usage 

# OPEN THE TERMINAL WHERE YOU DOWNLOADED THE ARRH FILE 


### Method 1: Command Prompt / Terminal (Recommended)




### 1. Encryption AND Decryption (`ARRH.py`)

Save the script as `ARRH.py` and run it using one of the methods below.


##### Windows
```cmd
python ARRH.py
```

##### macOS / Linux

```bash
python3 ARRH.py
```

#### Method 2: Double Click (Windows)

1. Right-click `ARRH.py`
2. Select **Open With**
3. Choose **Python**

### What the Script Does
* Decrypt or Encrypt hidden messages from someone you know

* Skips common system files and extensions
* Creates `.backup` 
* Generates a `SALT.KEY` file for decryption




## Important Notes

* Do not delete `SALT.KEY`; it is required for Decryption and Encryption .
* Keep `.backup` files until decryption is verified.
* Avoid running the encryptor or decryptor multiple times on the same files.
* Test the script on sample files before using important data.


## Troubleshooting (Windows)

| Problem                    | Solution                                                           |
| -------------------------- | ------------------------------------------------------------------ |
| `python is not recognized` | Use the full Python path, such as `C:\\Python\\python.exe ARRH.py` |
| Permission Error           | Run Command Prompt as Administrator                                |
| `ModuleNotFoundError`      | Reinstall the dependency using `pip install cryptography`          |
| Script closes immediately  | Run the script from Command Prompt instead of double-clicking      |

---

## Security Details

* Encryption Algorithm: AES-256-GCM
* Key Derivation Function: PBKDF2-HMAC-SHA256
* Iterations: 600,000
* Nonce Size: 12 bytes
* Salt Size: 16 bytes

---

## Disclaimer

This project is intended for educational and personal Use it only on systems and files you own or are authorized to manage. The author is not responsible for misuse, unauthorized activity.
