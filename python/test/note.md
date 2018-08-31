
## Lib
#### Quantra
- https://www.quantlib.org/download.shtml
- https://quantra.io/

#### string format usage
- https://pyformat.info/

## Install
    "pip install ." for development branch 
    https://github.com/vnpy/vnpy.git
    
#### Talib
    https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib


#### Android
    pip install -U setuptools
    install mongoDB: https://www.mongodb.com/download-center#atlas


## Google Console
- download FutuOpenD_1.02_Ubuntu16.04.tar.gz from QQ and upload to Google Console 
- run ```tar xf FutuOpenD_1.02_Ubuntu16.04.tar.gz```
- ```python3 -m pip install futuquant```

#### Talib in google Console
- download ta-lib from https://mrjbq7.github.io/ta-lib/install.html
```
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ~/ta-lib/
./configure --prefix=/usr
make
sudo make install
python3 -m pip install numpy 
python3 -m pip install --upgrade --force-reinstall Ta-Lib

#https://stackoverflow.com/questions/45406361/importerror-libta-lib-so-0-cannot-open-shared-object-file-no-such-file-or-dir
```

#### telegram 
```python3 -m pip insatll python-telegram-bot```

## Python 2/3 issue
C:\ProgramData\Anaconda3\Lib\site-packages\vnpy\rpc\vnrpc.py
```
import pickle
cPickle = pickle
```

- File "C:\ProgramData\Anaconda3\lib\site-packages\vnpy\trader\app\ctaStrategy\ctaBacktesting.py", line 403
- File "C:\ProgramData\Anaconda3\lib\site-packages\vnpy\trader\app\ctaStrategy\ctaBacktesting.py", line 864

```
add list(...):
```
