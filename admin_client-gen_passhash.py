import hashlib
import getpass

def generate_passhash_key():
    # Prompt for password input (hidden)
    password = getpass.getpass("Enter your password: ")
    
    # Encode the password to bytes
    password_bytes = password.encode('utf-8')
    
    # Generate SHA-256 hash
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    
    # Write the hash to 'passhash.key'
    with open("passhash.key", "w") as f:
        f.write(sha256_hash)
    
    print("Password hash written to 'passhash.key'.")

if __name__ == "__main__":
    generate_passhash_key()
