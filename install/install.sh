#!/usr/bin/env bash
echo please copy the latest FutuOpenD_1.03_Ubuntu16.04.tar.gz to ~/

cd ~
tar -xzf ~/FutuOpenD_1.03_Ubuntu16.04.tar.gz
tar -xzf ~/ckquant/install/ta-lib-0.4.0-src.tar.gz


# https://www.itzgeek.com/how-tos/mini-howtos/add-apt-repository-command-not-found-debian-ubuntu-quick-fix.html
 sudo apt-get install -y software-properties-common
# http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/
 sudo add-apt-repository ppa:jonathonf/python-3.6
 sudo apt-get update
 sudo apt-get install python3.6
 sudo apt-get install python3-pip
 sudo apt-get install python3.6-dev
 sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
 sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2

# install talib
# https://stackoverflow.com/questions/45406361/importerror-libta-lib-so-0-cannot-open-shared-object-file-no-such-file-or-dir
cd ~/ta-lib/
./configure --prefix=/usr
make
sudo make install
python3 -m pip install --upgrade Ta-Lib
pip install numpy

# install futuquant
pip3 install futuquant
python3 -m pip install -r ~/ckquant/requirements.txt

