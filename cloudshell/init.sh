#!/usr/bin/env bash
cd ~
rm -r ta-lib
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ~/ta-lib/
./configure --prefix=/usr
make
sudo make install
#python3 -m pip install numpy 
python3 -m pip install --upgrade --force-reinstall Ta-Lib



#https://stackoverflow.com/questions/45406361/importerror-libta-lib-so-0-cannot-open-shared-object-file-no-such-file-or-dir