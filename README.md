# miceHands

miceHands is a Python script for controlling your mouse with hand gestures

## Installation

Required python 3.6 for [windows ](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe) or linux (sudo apt-get install python3.6)

clone this repository using

```bash
git clone https://github.com/nishantsnair/miceHands.git
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

To use virtual environment first install with pip

```bash
pip install virtualenv
```

then create a virtual environment with virtualenv 
```bash
virtualenv -p "path to python 3.6" handsenv
```
source the environment in command prompt with

```bash
handsenv/scripts/activate
```

install reqirements with
```bash
pip install -r requirements.txt
```


## Usage

run the script with 

```bash
python detectHands.py
```
for mouse control with hands and
```bash
python detectPose.py
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)