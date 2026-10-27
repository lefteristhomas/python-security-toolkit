import hashlib
import os
import math
import pyotp

# ================== ΚΟΙΝΟΙ ΑΛΓΟΡΙΘΜΟΙ ==================

HASH_ALGOS = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA3": hashlib.sha3_256
}

CHOICE_TO_ALGO = {
    "1": "MD5",
    "2": "SHA1",
    "3": "SHA256",
    "4": "SHA3"
}

# ================== ΜΕΡΟΣ Α: HASH / ΑΚΕΡΑΙΟΤΗΤΑ ==================

def read_file(filename):
    try:
        with open(filename, "rb") as f:
            return f.read()
    except IOError:
        print("Το αρχείο δεν βρέθηκε!")
        return None

def calculate_hash(data, algorithm):
    return HASH_ALGOS[algorithm](data).hexdigest()

def save_hash_to_file(filename, hash_value, algorithm):
    hash_file = f"{filename}.{algorithm}.hash"
    with open(hash_file, "w") as f:
        f.write(hash_value)
    print(f"Το hash αποθηκεύτηκε στο {hash_file}")

def check_integrity(filename, algorithm):
    data = read_file(filename)
    if data is None:
        return

    if algorithm not in HASH_ALGOS:
        print("Άγνωστος αλγόριθμος")
        return

    current_hash = calculate_hash(data, algorithm)
    hash_file = f"{filename}.{algorithm}.hash"

    try:
        with open(hash_file, "r") as f:
            stored_hash = f.read().strip()

        print(f"\nΑποθηκευμένο hash: {stored_hash}")
        print(f"Τρέχον hash: {current_hash}")
        print(" Το αρχείο ΔΕΝ έχει τροποποιηθεί!" if current_hash == stored_hash else " Το αρχείο ΕΧΕΙ αλλοιωθεί!")
    except FileNotFoundError:
        print(f"Δεν βρέθηκε αρχείο hash: {hash_file}")

def generate_salt(length=16):
    return os.urandom(length)

def calculate_salted_hash(data, algorithm, salt):
    return calculate_hash(salt + data, algorithm) if algorithm in HASH_ALGOS else None

def save_salted_hash_to_file(filename, hash_value, algorithm, salt):
    hash_file = f"{filename}.{algorithm}.salted.hash"
    with open(hash_file, "w") as f:
        f.write(f"Algorithm: {algorithm}\nHash: {hash_value}\nSalt: {salt.hex()}\n")
    print(f"Το salted hash αποθηκεύτηκε στο {hash_file}")

def read_salted_hash_from_file(hash_filename):
    try:
        with open(hash_filename, "r") as f:
            lines = f.readlines()

        hash_value = None
        salt_hex = None

        for line in lines:
            if line.startswith("Hash:"):
                hash_value = line.replace("Hash:", "").strip()
            elif line.startswith("Salt:"):
                salt_hex = line.replace("Salt:", "").strip()

        if hash_value and salt_hex:
            return hash_value, bytes.fromhex(salt_hex)

        return None, None
    except Exception as e:
        print(f"Σφάλμα κατά την ανάγνωση του αρχείου hash: {e}")
        return None, None

def check_salted_integrity(filename, algorithm):
    print(f"\n--- Έλεγχος Ακεραιότητας με Salt για {filename} ---")

    data = read_file(filename)
    if data is None:
        return

    hash_file = f"{filename}.{algorithm}.salted.hash"
    stored_hash, salt = read_salted_hash_from_file(hash_file)

    if stored_hash is None:
        print(f"Δεν βρέθηκε αρχείο salted hash: {hash_file}")
        return

    current_hash = calculate_salted_hash(data, algorithm, salt)

    print(f"\nΑποθηκευμένο salted hash: {stored_hash}")
    print(f"Τρέχον salted hash: {current_hash}")
    print(f"Salt που χρησιμοποιήθηκε: {salt.hex()}")

    if current_hash == stored_hash:
        print("\n ΕΠΙΤΥΧΙΑ: Το αρχείο ΔΕΝ έχει τροποποιηθεί!")
    else:
        print("\n ΑΠΟΤΥΧΙΑ: Το αρχείο ΕΧΕΙ αλλοιωθεί!")

# ================== ΜΕΡΟΣ Β: ΕΝΤΡΟΠΙΑ ==================

def calculate_entropy(data):
    if not data:
        return 0

    total_bytes = len(data)
    frequency = [0] * 256

    for byte in data:
        frequency[byte] += 1

    entropy = 0
    for count in frequency:
        if count > 0:
            p = count / total_bytes
            entropy -= p * math.log2(p)

    return entropy

def display_entropy_result(entropy, filename):
    print("\n" + "=" * 60)
    print("ΑΠΟΤΕΛΕΣΜΑ ΕΝΤΡΟΠΙΑΣ".center(60))
    print("=" * 60)
    print(f"Αρχείο: {filename}")
    print(f"Τιμή εντροπίας: {entropy:.4f} bits (από 0 έως 8)")
    print("-" * 60)
    print("ΕΡΜΗΝΕΙΑ:")

    if entropy > 7.5:
        print("Πολύ υψηλή τυχαιότητα")
        print("  → Πιθανώς κρυπτογραφημένο ή συμπιεσμένο αρχείο")
    elif entropy > 6:
        print("Υψηλή τυχαιότητα")
        print("  → Δύσκολο να προβλεφθούν τα δεδομένα")
    elif entropy > 4:
        print("Μέτρια τυχαιότητα")
        print("  → Μίξη από διαφορετικά είδη δεδομένων")
    elif entropy > 2:
        print("Χαμηλή τυχαιότητα")
        print("  → Πιθανώς απλό κείμενο ή δομημένα δεδομένα")
    else:
        print("Πολύ χαμηλή τυχαιότητα")
        print("  → Ομοιόμορφα δεδομένα (π.χ. κενό αρχείο)")

    print("=" * 60)

def part_b():
    print("\n" + "=" * 60)
    print("ΜΕΡΟΣ Β: Υπολογισμός και Ανάλυση Εντροπίας")
    print("=" * 60)

    filename = input("Δώστε το όνομα του αρχείου για υπολογισμό εντροπίας: ")
    data = read_file(filename)

    if data is not None:
        print(f"Μέγεθος αρχείου: {len(data)} bytes")
        print("Υπολογισμός εντροπίας...")
        display_entropy_result(calculate_entropy(data), filename)

# ================== ΜΕΡΟΣ Γ: 2FA ==================

SECRET_KEY = None

def generate_secret_key():
    global SECRET_KEY
    SECRET_KEY = pyotp.random_base32()
    print(f"\n Μυστικό κλειδί δημιουργήθηκε: {SECRET_KEY}")
    print("   (Σημείωση: Σε πραγματική εφαρμογή, αυτό αποθηκεύεται με ασφάλεια)")
    return SECRET_KEY

def generate_otp():
    if SECRET_KEY is None:
        print(" Δεν έχει δημιουργηθεί μυστικό κλειδί!")
        return None
    return pyotp.TOTP(SECRET_KEY).now()

def verify_otp(user_code):
    if SECRET_KEY is None:
        print(" Δεν έχει δημιουργηθεί μυστικό κλειδί!")
        return False
    return pyotp.TOTP(SECRET_KEY).verify(user_code, valid_window=1)

def two_factor_auth():
    print("\n" + "=" * 60)
    print("ΑΥΘΕΝΤΙΚΟΠΟΙΗΣΗ ΔΥΟ ΠΑΡΑΓΟΝΤΩΝ (2FA)".center(60))
    print("=" * 60)

    if SECRET_KEY is None:
        print("\n  Δεν υπάρχει μυστικό κλειδί. Δημιουργία νέου...")
        generate_secret_key()

    otp_code = generate_otp()
    if otp_code is None:
        return False

    print(f"\n Ο κωδικός μιας χρήσης (OTP) είναι: {otp_code}")
    print("   (Σημείωση: Σε πραγματική εφαρμογή, αυτό στέλνεται στο κινητό)")

    user_input = input("\nΕισάγετε τον κωδικό OTP: ").strip()

    if verify_otp(user_input):
        print("\n ΕΠΙΤΥΧΙΑ: Η αυθεντικοποίηση 2FA ήταν επιτυχής!")
        print("   Η πρόσβαση επιτρέπεται.")
        return True
    else:
        print("\n ΑΠΟΤΥΧΙΑ: Λανθασμένος κωδικός OTP!")
        print("   Η πρόσβαση απορρίπτεται.")
        return False

def two_factor_auth_only():
    print("\n" + "=" * 60)
    print("ΔΟΚΙΜΗ 2FA".center(60))
    print("=" * 60)
    two_factor_auth()

# ================== ΜΕΡΟΣ Α: MAIN ΛΕΙΤΟΥΡΓΙΑ ==================

def part_a():
    print("=" * 60)
    print("ΜΕΡΟΣ Α: Υπολογισμός Hash και Έλεγχος Ακεραιότητας")
    print("=" * 60)
    print("\n  Για πρόσβαση σε αυτή τη λειτουργία απαιτείται 2FA")

    if not two_factor_auth():
        print("\nΔεν ήταν δυνατή η πρόσβαση. Επιστροφή στο κυρίως μενού.")
        return

    filename = input("\nΔώστε το όνομα του αρχείου: ")
    data = read_file(filename)

    if data is None:
        return

    print(f"Μέγεθος: {len(data)} bytes")
    use_salt = input("\nΘέλετε να χρησιμοποιήσετε Salt για το hash; (y/n): ").lower()

    print("\nΕπιλέξτε αλγόριθμο:")
    print("1. MD5")
    print("2. SHA-1")
    print("3. SHA-256")
    print("4. SHA-3")
    print("5. Όλους")

    choice = input("Επιλογή (1-5): ")

    if use_salt == "y":
        if choice in CHOICE_TO_ALGO:
            algo = CHOICE_TO_ALGO[choice]
            salt = generate_salt()
            hash_value = calculate_salted_hash(data, algo, salt)

            print(f"\n Δημιουργήθηκε salt: {salt.hex()}")
            print(f"{algo} (με salt): {hash_value}")

            if input("Αποθήκευση salted hash? (y/n): ").lower() == "y":
                save_salted_hash_to_file(filename, hash_value, algo, salt)

            if input("\nΘέλετε να ελέγξετε την ακεραιότητα του αρχείου; (y/n): ").lower() == "y":
                check_salted_integrity(filename, algo)

        elif choice == "5":
            print("\n Υπολογισμός με Salt για όλους τους αλγόριθμους:")
            for algo in HASH_ALGOS:
                salt = generate_salt()
                hash_value = calculate_salted_hash(data, algo, salt)
                print(f"\n{algo}:")
                print(f"  Salt: {salt.hex()}")
                print(f"  Hash: {hash_value}")
        else:
            print("Μη έγκυρη επιλογή!")

    else:
        if choice in CHOICE_TO_ALGO:
            algo = CHOICE_TO_ALGO[choice]
            hash_value = calculate_hash(data, algo)
            print(f"{algo.replace('SHA1', 'SHA-1').replace('SHA256', 'SHA-256').replace('SHA3', 'SHA-3')}: {hash_value}")

            if input("Αποθήκευση hash? (y/n): ").lower() == "y":
                save_hash_to_file(filename, hash_value, algo)

        elif choice == "5":
            for algo in HASH_ALGOS:
                pretty = algo.replace("SHA1", "SHA-1").replace("SHA256", "SHA-256").replace("SHA3", "SHA-3")
                print(f"{pretty}: {calculate_hash(data, algo)}")
        else:
            print("Μη έγκυρη επιλογή!")

        if input("\nΘέλετε να ελέγξετε την ακεραιότητα του αρχείου; (y/n): ").lower() == "y":
            algo = input("Για ποιον αλγόριθμο; (MD5/SHA1/SHA256/SHA3): ")
            check_integrity(filename, algo)

def main():
    while True:
        print("\n" + "=" * 60)
        print("ΕΡΓΑΣΙΑ ΑΣΦΑΛΕΙΑ ΣΥΣΤΗΜΑΤΩΝ".center(60))
        print("=" * 60)
        print("\nΚΥΡΙΩΣ ΜΕΝΟΥ:")
        print("1. ΜΕΡΟΣ Α: Υπολογισμός Hash και Έλεγχος Ακεραιότητας (με Salt)")
        print("2. ΜΕΡΟΣ Β: Υπολογισμός Εντροπίας")
        print("3. ΜΕΡΟΣ Γ: Δοκιμή 2FA (Αυθεντικοποίηση)")
        print("4. Έξοδος")

        main_choice = input("\nΕπιλέξτε ενότητα (1-4): ")

        if main_choice == "1":
            part_a()
        elif main_choice == "2":
            part_b()
        elif main_choice == "3":
            two_factor_auth_only()
        elif main_choice == "4":
            print("\nΈξοδος από το πρόγραμμα...")
            break
        else:
            print("Μη έγκυρη επιλογή! Παρακαλώ επιλέξτε 1, 2, 3 ή 4.")

        input("\nΠατήστε Enter για να συνεχίσετε...")

if __name__ == "__main__":
    main()