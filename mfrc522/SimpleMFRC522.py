# Code by Simon Monk https://github.com/simonmonk/

from . import MFRC522

  
class SimpleMFRC522:

  READER = None
  
  KEY = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
  BLOCK_ADDRS = [8, 9, 10]
  
  def __init__(self):
    self.READER = MFRC522()
  
  def read(self):
      id, text = self.read_no_block()
      while not id:
          id, text = self.read_no_block()
      return id, text

  def read_id(self):
    id = self.read_id_no_block()
    while not id:
      id = self.read_id_no_block()
    return id

  def read_id_no_block(self):
      (status, TagType) = self.READER.mfrc522_request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None
      (status, uid) = self.READER.mfrc522_anticoll()
      if status != self.READER.MI_OK:
          return None
      return self.uid_to_num(uid)
  
  def read_no_block(self):
    (status, TagType) = self.READER.mfrc522_request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None, None
    (status, uid) = self.READER.mfrc522_anticoll()
    if status != self.READER.MI_OK:
        return None, None
    id = self.uid_to_num(uid)
    self.READER.mfrc522_select_tag(uid)
    status = self.READER.mfrc522_auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
    data = []
    text_read = ''
    if status == self.READER.MI_OK:
        for block_num in self.BLOCK_ADDRS:
            block = self.READER.mfrc522_read(block_num)
            if block:
            		data += block
        if data:
             text_read = ''.join(chr(i) for i in data)
    self.READER.mfrc522_stop_crypto1()
    return id, text_read
    
  def write(self, text):
      id, text_in = self.write_no_block(text)
      while not id:
          id, text_in = self.write_no_block(text)
      return id, text_in

  def write_no_block(self, text):
      (status, TagType) = self.READER.mfrc522_request(self.READER.PICC_REQIDL)
      if status != self.READER.MI_OK:
          return None, None
      (status, uid) = self.READER.mfrc522_anticoll()
      if status != self.READER.MI_OK:
          return None, None
      id = self.uid_to_num(uid)
      self.READER.mfrc522_select_tag(uid)
      status = self.READER.mfrc522_auth(self.READER.PICC_AUTHENT1A, 11, self.KEY, uid)
      self.READER.mfrc522_read(11)
      if status == self.READER.MI_OK:
          data = bytearray()
          data.extend(bytearray(text.ljust(len(self.BLOCK_ADDRS) * 16).encode('ascii')))
          i = 0
          for block_num in self.BLOCK_ADDRS:
            self.READER.mfrc522_write(block_num, data[(i * 16):(i + 1) * 16])
            i += 1
      self.READER.mfrc522_stop_crypto1()
      return id, text[0:(len(self.BLOCK_ADDRS) * 16)]
      
  def uid_to_num(self, uid):
      n = 0
      for i in range(0, 5):
          n = n * 256 + uid[i]
      return n
