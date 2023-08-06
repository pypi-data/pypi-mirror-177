from nacl.signing import SigningKey, VerifyKey
from base58 import b58encode

def base_58_signing_key(key: SigningKey):
    """Converts a signing key to base58"""
    return b58encode(key._signing_key).decode('utf-8')

def base_58_verify_key(key: VerifyKey):
    """Converts a verify key to base58"""
    return b58encode(key.encode()).decode('utf-8')

def format_ed25519_key(key: str):
    """Formats ed25519 key for NEAR PROTOCOL"""
    return f"ed25519:{key}"