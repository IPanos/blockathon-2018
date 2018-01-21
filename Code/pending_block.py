from Crypto.Hash.MD5 import MD5Hash
from Crypto.Signature.PKCS1_v1_5 import PKCS115_SigScheme

# pending block contents are:
# - parent signature
# - registration document (including public keys of signatories)
# - triple of pending signatures (first entry must be bureaucratic signature)

#TODO
# implement logic for adding a signature to the correct position in the pending_signatures triple


class PendingBlock:

    def __init__(self, rsa_key, registration_document, blockchain):
        self.parent_signature = blockchain[-1].get_signature()
        self.registration_document = registration_document
        encoded_registration_document = PendingBlock.encode_into_byte_string(registration_document)
        encoded_parent_signature = PendingBlock.encode_into_byte_string(self.parent_signature)
        hash_value = self.hash_record_contents(self, encoded_registration_document, encoded_parent_signature)
        self._pending_signatures = (self.sign(rsa_key, hash_value), '', '')

    @classmethod
    def encode_into_byte_string(cls, message):
        return message.encode('utf-8', 'backslashreplace')

    @classmethod
    def hash_record_contents(cls, registration_document, parent_signature):
        hash_algorithm = MD5Hash()
        hash_algorithm.update(registration_document+parent_signature)
        return hash_algorithm.digest()

    @classmethod
    def sign(cls, rsa_key, hash_value):
        sig_scheme = PKCS115_SigScheme(rsa_key)
        signature = sig_scheme.sign(hash_value)
        return signature[0]

    def get_pending_signatures(self):
        return self._pending_signatures