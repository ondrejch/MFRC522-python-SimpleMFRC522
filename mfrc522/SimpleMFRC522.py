from . import MFRC522


class SimpleMFRC522:
    KEYS = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    BLOCK_ADDRESSES = [8, 9, 10]

    def __init__(self):
        self.reader = MFRC522()

    def read(self):
        while True:
            tag_id, text = self.read_no_block()
            if tag_id:
                return tag_id, text

    def read_id(self):
        while True:
            id_tag = self.read_id_no_block()
            if id_tag:
                return id_tag

    def read_id_no_block(self):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None
        status, uid = self.reader.mfrc522_anticoll()
        return None if status != self.reader.MI_OK else self.uid_to_number(uid)

    def read_no_block(self):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        status, uid = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        tag_id = self.uid_to_number(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(
            self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid
        )
        text_read = ""
        if status == self.reader.MI_OK:
            data = [
                self.reader.mfrc522_read(address)
                for address in self.BLOCK_ADDRESSES
                if self.reader.mfrc522_read(address)
            ]
            text_read = "".join(chr(i) for i in data)
        self.reader.mfrc522_stop_crypto1()
        return tag_id, text_read

    def write(self, text):
        while True:
            tag_id, text_in = self.write_no_block(text)
            if tag_id:
                return tag_id, text_in

    def write_no_block(self, text):
        status, _ = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        status, uid = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        tag_id = self.uid_to_number(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(
            self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid
        )
        self.reader.mfrc522_read(11)
        if status == self.reader.MI_OK:
            data = bytearray()
            data.extend(
                bytearray(text.ljust(len(self.BLOCK_ADDRESSES) * 16).encode("ascii"))
            )
            for index, block_num in enumerate(self.BLOCK_ADDRESSES):
                self.reader.mfrc522_write(
                    block_num, data[(index * 16) : (index + 1) * 16]
                )
        self.reader.mfrc522_stop_crypto1()
        return tag_id, text[: len(self.BLOCK_ADDRESSES) * 16]

    @staticmethod
    def uid_to_number(uid):
        number = 0
        for index, character in enumerate(uid):
            number = number * 256 + character
            if index == 4:
                return number
