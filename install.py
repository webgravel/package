#!/usr/bin/env python2
from __future__ import print_function

import gravelfile
import glob
import sys
import os
import yaml
import subprocess

def warn(*args, **kwargs):
    kwargs['file'] = sys.stderr
    print(*args, **kwargs)

class LocalRepo:
    def __init__(self, path):
        self.path = path

    def get_package(self, name):
        names = glob.glob('%s/*/%s.gravelpkg' % (self.path, name))
        if not names:
            raise IOError('package %s not found' % name)
        if len(names) > 1:
            warn('found multiple instances of %s' % name)
        return open(names[0], 'rb').read()

class Installer:
    def __init__(self, home):
        self.home = home
        self.load_config()

    def load_config(self):
        self.config = yaml.safe_load(open(self.home + '/config.yaml'))
        url = self.config['repo']
        if url.startswith('ssh://'):
            self.repo = SSHRepo(url)
        else:
            self.repo = LocalRepo(url)

        self.gpg = gravelfile.GPG(path=self.config['gpghome'])

    def list_packages(self):
        pkgs = []
        for name in os.listdir(self.home):
            if os.path.exists(self.home + '/' + name + '/.installed'):
                pkgs.append(name)
        return pkgs

    def install(self, name, upgrade=False):
        installed = name in self.list_packages()
        if not upgrade and installed:
            return

        print('installing %s...' % name)
        if installed:
            Package(self, name).trigger('preupgrade')

        dest = self.home + '/' + name
        gravelfile.unpack(data=self.repo.get_package(name), dest=dest, gpg=self.gpg)

        pkg = Package(self, name)
        pkg.install_dep()

        if installed:
            pkg.trigger('postupgrade')
        else:
            pkg.trigger('first-preinstall')

        pkg.trigger('preinstall')
        with open(dest + '/.installed', 'a'): pass
        pkg.trigger('postinstall')
        pkg.restart()

class Package:
    def __init__(self, installer, name):
        self.installer = installer
        self.name = name
        self.path = self.installer.home + '/' + name
        self.gravelfile = yaml.safe_load(open(self.path + '/Gravelfile'))

    def trigger(self, name):
        print('running trigger %s for %s... [not really]' % (name, self.name))

    def install_dep(self):
        packages = self.gravelfile.get('requires', '').split()
        for pkg in packages:
            self.installer.install(pkg)
        packages = self.gravelfile.get('requires-apt', '').split()
        if packages:
            print('installing APT dependencies for %s...' % self.name)
            subprocess.check_call(['sudo', 'apt-get', 'install', '-qy'] + packages)

    def restart(self):
        self.stop()
        self.start()

    def stop(self):
        pass #os.kill(self._get_pid(), 15)

    def start(self):
        pass

    def _get_pid(self):
        path = _get_pid_file()
        try:
            return open(path).read().strip()
        except IOError:
            return 0

    def _get_pid_file(self):
        run = self.installer.config['run']
        return run + '/' + self.name + '.pid'

if __name__ == '__main__':
    home = os.environ.get('GRAVELHOME', '/gravel/pkg')
    actions = 'install|upgrade|start|stop|restart'.split('|')
    action = sys.argv[1]
    if len(sys.argv) != 3 or action not in actions:
        sys.exit('usage: install.py %s pkg' % '|'.join(actions))
    installer = Installer(home=home)
    if action in ('upgrade', 'install'):
        upgrade = sys.argv[1] == 'upgrade'
        installer.install(sys.argv[2], upgrade=upgrade)
