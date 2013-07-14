GHOME=~/gravel
REPO=gravelrepo@v0.atomshare.net:/home/gravelrepo/

packages=$GHOME/*/*.gravelpkg
tmp=`mktemp -d`
for pkg in $packages; do
    echo $pkg
    cp $pkg $tmp/
done

rsync -r --progress $tmp/ $REPO
cd ~
rm -r $tmp
