GHOME=~/gravel
REPO_SRV=gravelrepo@v0.atomshare.net
REPO_PATH=/home/gravelrepo/

packages=$GHOME/*/*.gravelpkg
tmp=`mktemp -d`
for pkg in $packages; do
    echo $pkg
    cp $pkg $tmp/
done

rsync -r --progress $tmp/ $REPO_SRV:$REPO_PATH
ssh $REPO_SRV chmod 644 $REPO_PATH'/*.gravelpkg'
cd ~
rm -r $tmp
