# python-security-toolkit
Educational Python CLI for file hashing, integrity verification, salted hashing, Shannon entropy analysis, and TOTP demonstrations.

The project demonstrates file hashing, integrity verification, salted hashing, Shannon entropy analysis, and time-based one-time passwords (TOTP). It provides an interactive menu, with prompts currently written in Greek.

## Main Features

### 1. File Hashing and Integrity Verification

The application reads a file and calculates its hash using **MD5, SHA-1, SHA-256, or SHA3-256**. Users can select one algorithm or display the results of all four.

A hash is a fixed-length fingerprint of the file's contents. Changing the contents will generally produce a different hash, making it useful for detecting modifications.

When selecting a single algorithm, users can save the result to a `.hash` file. The integrity check recalculates the original file's hash and compares it with the saved value to report whether the contents have changed.

### 2. Salted Hashing

Users can optionally enable a randomly generated **16-byte salt**. The application places this random value before the file's contents and hashes the combined data:

```text
hash(salt + file_data)
```

Different salts produce different hashes for the same input. For a single selected algorithm, the hash and salt can be saved together in a `.salted.hash` file. Verification reuses the saved salt to reproduce the calculation.

Selecting all algorithms displays a salted hash for each algorithm but does not save the results.

### 3. Shannon Entropy Analysis

The application calculates a file's **Shannon entropy** by counting how frequently each byte value appears.

The result ranges from **0 to 8 bits per byte**:

- **Lower values** indicate more repetitive or predictable data.
- **Higher values** indicate a more evenly distributed set of byte values, often found in compressed or encrypted files.

The program displays the calculated value and a brief interpretation. Entropy alone does not prove that a file is encrypted or secure.

### 4. TOTP Demonstration

Using **PyOTP**, the application generates a secret key and a time-based one-time password. The user enters the displayed code, and the application verifies it before allowing access to the hashing section.

This process can also be tested through a separate menu option. The secret remains in memory during execution and is regenerated after restarting the application.

## How It Works

The main menu provides four options:

1. **Hashing and integrity verification:** verify an OTP, choose a file, enable or disable salt, select an algorithm, and optionally save or verify a hash.
2. **Entropy analysis:** choose a file and display its entropy.
3. **TOTP demonstration:** generate and verify a temporary code.
4. **Exit:** close the application.

For file inputs, enter a filename or path. For `(y/n)` prompts, enter `y` for yes or `n` for no.

## Requirements and Execution

The project uses Python 3 and the standard libraries `hashlib`, `os`, and `math`. Its only external dependency is `pyotp`.

Install the dependency:

```bash
python -m pip install pyotp
```

Run the application:

```bash
python security_systems.py
```

If your system uses `python3`, replace `python` with `python3`.

## Educational Notes

The authentication feature is a **TOTP demonstration**, rather than a complete two-factor authentication system: the secret and code are displayed in the same terminal, and no separate first factor is implemented.

MD5 and SHA-1 are included for educational comparison. Salted hashing here is not intended for password storage, and file integrity verification assumes that the saved reference hash is trustworthy.
