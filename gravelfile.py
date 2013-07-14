import yaml
import gnupg
import os
import io
import tarfile

class GPG:
    def __init__(self, path=os.path.expanduser('~/.gravel/gpg')):
        self.gpg = gnupg.GPG(gnupghome=path)

    def verify_and_get(self, data):
        verification = self.gpg.verify(data)
        if not verification.valid:
            raise VerificationError()
        return self.gpg.decrypt(data).data

class VerificationError(Exception):
    pass

def unpack(data, dest, gpg):
    pkg_data = gpg.verify_and_get(data)
    tar = tarfile.open(fileobj=io.BytesIO(pkg_data), mode='r')
    tar.extractall(dest)
