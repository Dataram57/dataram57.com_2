import os
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519



folder_path = "result"
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()



def sha256_of_file(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

for root, dirs, files in os.walk(folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)
        rel_file_path = file_path[len(folder_path) + 1:]
        # Hashes
        path_hash = hashlib.sha256(rel_file_path.encode()).hexdigest()
        file_hash = sha256_of_file(file_path)
        asset = rel_file_path.encode().hex() + file_hash
        asset_hash = hashlib.sha256(bytes.fromhex(asset)).hexdigest()
        # Prints
        print("================ " + file_path + " ================")
        print("_Path:", rel_file_path)
        print("_FileHash:", file_hash)
        print("_Asset:", asset)
        print("AssetHash:", asset_hash)
        # Signing everything again should be avoided as some signature schemes have limits
        # Sign
        sign = private_key.sign(bytes.fromhex(asset_hash)).hex()
        # Print Sign
        print("Sign:", sign)
        #check sign
        try:
            expr = hashlib.sha256(bytes.fromhex(rel_file_path.encode().hex() + file_hash)).digest()
            public_key.verify(bytes.fromhex(sign), expr)
            print("✅ Sign verified.")
        except Exception:
            print("❌ Sign failed to verify.")

