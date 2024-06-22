# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

import os
import hmac
import math
import sys
import base64
import Crypto
import hashlib
import Crypto.Cipher
from io import StringIO
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from collections import OrderedDict

DATA_LEN = 4
BUCKET_SIZE = 16


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

    # Request from the client to read a path to a leaf from Storage field
    def read_path(self, path):
        data = []
        for bucket_id in path:
            data.extend(self.storage[bucket_id])
        return data

    # Request from the client to update a path to a leaf from Storage field
    def write_path(self, path, data):
        for bucket_id, blocks in zip(path, data):
            self.storage[bucket_id] = blocks

    # Request from the client to get the size of a bucket inside the Storage
    def get_bucket_size(self, bucket_id):
        return len(self.storage[bucket_id])

    # Request from the client to append an item to a bucket inside the Storage
    def add_to_bucket(self, bucket_id, entry):
        self.storage[bucket_id].append(entry)

    # Request from the client to share a key for encryption
    def share_key(self):
        return self.key
