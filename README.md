!Caution! Do not use, the code is under development
====================================================

Original code from [pimylifeup](https://github.com/YudiNz/MFRC522-python-SimpleMFRC522).
`RPi.GPIO` don't support the Raspberry Pi 5. In this fork I refactored the code to support also the Raspberry Pi 5.

Create development environment
---------------------

For example this should work. You don't have to use `nano`, you can use your favorite editor. Add the example code below 
in `read_tag.py`.
```bash
mkdir mfrc522_test
python -m venv ~/mfrc522_test/
. ~/mfrc522_test/bin/activate
(mfrc522_test) [dennis@dennis ~]$ mkdir ~/mfrc522_test/src
(mfrc522_test) [dennis@dennis ~]$ git clone https://github.com/Dennis-89/MFRC522-python-SimpleMFRC522.git ~/mfrc522_test/src/
Klone nach '/home/dennis/mfrc522_test/src'...
remote: Enumerating objects: 205, done.
remote: Counting objects: 100% (154/154), done.
remote: Compressing objects: 100% (71/71), done.
remote: Total 205 (delta 92), reused 140 (delta 83), pack-reused 51
Empfange Objekte: 100% (205/205), 57.96 KiB | 1.29 MiB/s, fertig.
Löse Unterschiede auf: 100% (93/93), fertig.

python ~/mfrc522_test/src/setup.py install
nano ~/mfrc522_test/read_tag.py
python ~/mfrc522_test/read_tag.py
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
