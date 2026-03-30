from fastapi import FastAPI, Response
from Crypto.Cipher import AES
import json
import binascii

app = FastAPI()

# Configuration
KEY = b"maggikhalo".ljust(32, b'\0')

def decrypt_internal(encrypted_str: str) -> dict:
    """Helper to decrypt the DeltaStudy format internally."""
    try:
        iv_hex, payload_hex = encrypted_str.split(':')
        iv = binascii.unhexlify(iv_hex)
        payload = binascii.unhexlify(payload_hex)
        
        # Tag is the last 16 bytes
        ciphertext = payload[:-16]
        tag = payload[-16:]
        
        cipher = AES.new(KEY, AES.MODE_GCM, nonce=iv)
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return json.loads(decrypted_bytes.decode('utf-8'))
    except Exception as e:
        return {"error": f"Decryption failed: {str(e)}"}

@app.get("/")
def home():
    return {"message": "Server-Side Decryption Active"}

@app.get("/api/pw/batches")
def get_batches_decrypted():
    # 1. This represents the encrypted data you currently have
    # (In a real app, you might fetch this from another database or API)
    encrypted_source = "d2658440972349fb46d8aa9f:2c1da5b309c7f48442253c13e9677fc913ccb9aea7159fbdb8b905f85a25fa648011f4c052e8be100d0686740ae367cf15c2e307b042f9044d9e53d709aa736b84ab1011c1512dc23ab3cfd4191e"
    
    # 2. Decrypt it right here on the server
    decrypted_data = decrypt_internal(encrypted_source)
    
    # 3. Return the clean JSON directly to the user
    return decrypted_data
