!Caution! Do not use, the code is under development
====================================================

Original code from [pimylifeup](https://github.com/YudiNz/MFRC522-python-SimpleMFRC522).
`RPi.GPIO` don't support the Raspberry Pi 5. In this fork I refactored the code to support also the Raspberry Pi 5.

Create development environment
---------------------

For example this should work. You don't have to use `nano`, you can use your favorite editor. Add the example code below 
in `read_tag.py`.
```bash
dennis@test:~ $ mkdir mfrc522_test/src -p
dennis@test:~ $ python -m venv mfrc522_test/.venv
dennis@test:~ $ git clone https://github.com/Dennis-89/MFRC522-python-SimpleMFRC522.git mfrc522_test/src/
Cloning into 'mfrc522_test/src'...
remote: Enumerating objects: 211, done.
remote: Counting objects: 100% (160/160), done.
remote: Compressing objects: 100% (74/74), done.
remote: Total 211 (delta 96), reused 145 (delta 86), pack-reused 51 (from 1)
Receiving objects: 100% (211/211), 59.00 KiB | 1.34 MiB/s, done.
Resolving deltas: 100% (97/97), done.
dennis@test:~ $ . mfrc522_test/.venv/bin/activate
(.venv) dennis@test:~ $ pip install -U setuptools
(.venv) dennis@test:~ $ python mfrc522_test/src/setup.py install
(.venv) dennis@test:~ $ nano mfrc522_test/read_tag.py
(.venv) dennis@test:~ $ python mfrc522_test/read_tag.py
```

## Example Code

The following code will read a tag from the MFRC522

```python
from time import sleep
from mfrc522 import SimpleMFRC522


def main():
    reader = SimpleMFRC522()
    while True:
        print("Hold a tag near the reader")
        tag_id, text = reader.read()
        print(f'ID: {tag_id}\nText: {text}')
        sleep(1)

if __name__ == '__main__':
    main()
```

Original ReadMe-Description:
-----------------------------

# mfrc522

A python library to read/write RFID tags via the budget MFRC522 RFID module.

This code was published in relation to a [blog post](https://pimylifeup.com/raspberry-pi-rfid-rc522/) and you can find out more about how to hook up your MFRC reader to a Raspberry Pi there.

## Installation

Until the package is on PyPi, clone this repository and run `python setup.py install` in the top level directory.

## Example Code

The following code will read a tag from the MFRC522

```python
from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id,text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
```
