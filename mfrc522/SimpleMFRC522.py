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
        (status, TagType) = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None
        (status, uid) = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None
        return self.uid_to_num(uid)

    def read_no_block(self):
        (status, TagType) = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        (status, uid) = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid)
        data = []
        text_read = ""
        if status == self.reader.MI_OK:
            for block_num in self.BLOCK_ADDRESSES:
                block = self.reader.mfrc522_read(block_num)
                if block:
                    data += block
            if data:
                text_read = "".join(chr(i) for i in data)
        self.reader.mfrc522_stop_crypto1()
        return id, text_read

    def write(self, text):
        id, text_in = self.write_no_block(text)
        while not id:
            id, text_in = self.write_no_block(text)
        return id, text_in

    def write_no_block(self, text):
        (status, TagType) = self.reader.mfrc522_request(self.reader.PICC_REQIDL)
        if status != self.reader.MI_OK:
            return None, None
        (status, uid) = self.reader.mfrc522_anticoll()
        if status != self.reader.MI_OK:
            return None, None
        id = self.uid_to_num(uid)
        self.reader.mfrc522_select_tag(uid)
        status = self.reader.mfrc522_auth(self.reader.PICC_AUTHENT1A, 11, self.KEYS, uid)
        self.reader.mfrc522_read(11)
        if status == self.reader.MI_OK:
            data = bytearray()
            data.extend(
                bytearray(text.ljust(len(self.BLOCK_ADDRESSES) * 16).encode("ascii"))
            )
            i = 0
            for block_num in self.BLOCK_ADDRESSES:
                self.reader.mfrc522_write(block_num, data[(i * 16): (i + 1) * 16])
                i += 1
        self.reader.mfrc522_stop_crypto1()
        return id, text[0 : (len(self.BLOCK_ADDRESSES) * 16)]

    def uid_to_num(self, uid):
        n = 0
        for i in range(0, 5):
            n = n * 256 + uid[i]
        return n
