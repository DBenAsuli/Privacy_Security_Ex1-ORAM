# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

import os
import hmac
import math
import base64
import Crypto
import hashlib
import Crypto.Cipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from collections import OrderedDict

DATA_LEN = 4
BUCKET_SIZE = 4


class Server():
    N = 0

    def __init__(self, num_of_blocks, bucket_size=BUCKET_SIZE):
        self.N = num_of_blocks
        self.bucket_size = bucket_size
        self.tree_height = math.ceil(math.log2(num_of_blocks))
        self.num_of_buckets = 2 ** (self.tree_height + 1) - 1
        self.key = get_random_bytes(32)

        # The Storage is implemented as a list but functionally acts like a binary tree
        self.storage = [[] for _ in range(self.num_of_buckets)]

    def read_path(self, path):
        data = []
        for bucket_id in path:
            data.extend(self.storage[bucket_id])
        return data

    def write_path(self, path, data):
        for bucket_id, blocks in zip(path, data):
            self.storage[bucket_id] = blocks

    def share_key(self):
        return self.key

    def encrypt_block(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return base64.b64encode(nonce + tag + ciphertext).decode()

    def decrypt_block(self, encrypted_block):
        encrypted_data = base64.b64decode(encrypted_block)
        nonce = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
