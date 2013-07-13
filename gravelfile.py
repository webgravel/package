import yaml
import gnupg
import os

class GPG:
    def __init__(self, path=os.path.expanduser('~/.gravel/gpg')):
        self.gpg = gnupg.GPG(gnupghome=path)

    def verify_and_get(data):
        verification = self.gpg.verify(data)
        if not verification.valid:
            raise VerificationError()
        return self.gpg.decrypt(data)

class VerificationError(Exception):
    pass
