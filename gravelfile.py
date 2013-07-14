import yaml
import gnupg
import os
import io
import tarfile
import subprocess

class GPG:
    def __init__(self, path=os.path.expanduser('~/.gravel/gpg')):
        self.path = path
        self.cmd = ['gpg', '--homedir', self.path]

    def verify_and_get(self, input):
        result = subprocess.call(self.cmd + ['--verify'],
                                 stdin=open(input),
                                 stderr=open('/dev/null', 'w'))
        if result != 0:
            raise VerificationError()
        return subprocess.check_output(self.cmd + ['--decrypt'],
                                       stdin=open(input), stderr=open('/dev/null', 'w'))

class VerificationError(Exception):
    pass

def unpack(input, dest, gpg):
    pkg_data = gpg.verify_and_get(input)
    tar = tarfile.open(fileobj=io.BytesIO(pkg_data), mode='r')
    tar.extractall(dest)
