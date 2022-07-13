from secrets import token_bytes

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)


class Crypt:
    def __init__(self, pk_raw: bytes):
        self.private_key = X25519PrivateKey.from_private_bytes(pk_raw)
        self.public_key = self.private_key.public_key()
        self.random = token_bytes(32)

    def xored_nonce(self, nonce: bytes):
        return bytes([_a ^ _b for _a, _b in zip(nonce, self.random)])

    def encrypt(self, public_key: bytes, secret: bytes, nonce: bytes):
        shared_nonce = self.xored_nonce(nonce)
        shared_key = self.private_key.exchange(public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=shared_nonce[:20],
            info=None,
        ).derive(shared_key)
        aes = AESGCM(derived_key)
        return aes.encrypt(nonce=shared_nonce[-12:], data=secret, associated_data=None)

    def decrypt(self, public_key: bytes, secret: bytes, nonce: bytes):
        shared_nonce = self.xored_nonce(nonce)
        shared_key = self.private_key.exchange(public_key)
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=shared_nonce[:20],
            info=None,
        ).derive(shared_key)
        aes = AESGCM(derived_key)
        return aes.decrypt(nonce=shared_nonce[-12:], data=secret, associated_data=None)


private_key = X25519PrivateKey.generate().private_bytes(
    Encoding.Raw, PrivateFormat.Raw, NoEncryption()
)
crypt = Crypt(private_key)
