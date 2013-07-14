REPO=http://repo.gravel.atomshare.net
mkdir /gravel
mkdir /gravel/log /gravel/run /gravel/pkg /gravel/gpg
cd `mktemp -d`
wget $REPO/public.gpg || exit 1
wget $REPO/ownertrust.gpg || exit 1
chmod 700 /gravel/gpg
gpg --homedir=/gravel/gpg --import < public.gpg || exit 1
gpg --homedir=/gravel/gpg --import-ownertrust < ownertrust.gpg || exit
echo "repo: '$REPO'
run: /gravel/run
log: /gravel/pkg
gpghome: /gravel/gpg
" > /gravel/pkg/config.yaml
apt-get install -y python-gnupg python-yaml git htop sudo || exit 1
git clone https://github.com/webgravel/package || exit 1
cd package
./install.py install gravel-package || exit 1
ln -s /gravel/pkg/gravel-package/install.py /usr/local/bin/gravelpkg
