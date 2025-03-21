import itertools
import time
import os

# Define allowed character sets
uppercase_letters = ['A', 'B', 'C', 'D', 'E']
lowercase_letters = ['a', 'b', 'c', 'd', 'e']
digits = ['1', '2', '3', '4', '5']
special_symbols = ['$', '&', '%']

all_letters = uppercase_letters + lowercase_letters
all_characters = all_letters + digits + special_symbols

# Start timing execution
start_time = time.time()

# ✅ Get user input for password length
while True:
    try:
        password_length = int(input("Enter the password length (4, 5, 6): "))
        if password_length not in {4, 5, 6}:
            print("Only lengths 4, 5, or 6 are allowed for testing.")
        else:
            break
    except ValueError:
        print("Invalid input! Please enter a valid number.")

# ✅ Generate all possible passwords using itertools.product()
raw_passwords = itertools.product(all_characters, repeat=password_length)

# ✅ Function to check password validity
def is_valid(password):
    password = ''.join(password)  # Convert tuple to string
    
    # Must start with a letter (uppercase or lowercase)
    if password[0] not in all_letters:
        return False

    # Must contain at least one from each category
    has_upper = any(c in uppercase_letters for c in password)
    has_lower = any(c in lowercase_letters for c in password)
    has_digit = any(c in digits for c in password)
    has_special = any(c in special_symbols for c in password)

    if not (has_upper and has_lower and has_digit and has_special):
        return False

    # Must not contain more than 2 uppercase letters
    if sum(1 for c in password if c in uppercase_letters) > 2:
        return False

    # Must not contain more than 2 special symbols
    if sum(1 for c in password if c in special_symbols) > 2:
        return False

    return True

# ✅ Filter valid passwords
valid_passwords = ["".join(p) for p in raw_passwords if is_valid(p)]

# ✅ Define file path dynamically in the same directory as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script directory
output_file = os.path.join(BASE_DIR, "valid_passwords.txt")  # Define full file path

# ✅ Save valid passwords in the script’s directory
with open(output_file, "w") as f:
    for index, password in enumerate(valid_passwords, start=1):
        f.write(f"{index} {password}\n")

# ✅ Stop timing execution
end_time = time.time()
execution_time = round(end_time - start_time, 4)

# ✅ Print summary
print(f"\n✅ Generated {len(valid_passwords)} valid passwords.")
print(f"📁 Saved to: {output_file}")
print(f"⏳ Execution Time: {execution_time} seconds")