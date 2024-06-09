# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024
import math

import Crypto.Cipher
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
        self.buckets = [[] for _ in range(self.num_of_buckets)]

    def read_path(self, path):
        data = []
        for bucket_id in path:
            data.extend(self.buckets[bucket_id])
        return data

    def write_path(self, path, data):
        for bucket_id, blocks in zip(path, data):
            self.buckets[bucket_id] = blocks

    def store_data(self, id, data):
        pass

    def retrieve_data(self, id, data):
        pass

    def delete_data(self, id, data):
        pass


class DataBlock():
    data_len = DATA_LEN
    data = []
    is_valid_block = 0

    def __init__(self):
        # "data" will contain garbage upon initialization
        self.data = [chr(i) for i in range(0, DATA_LEN)]

    def set_data(self, chars):
        self.data = [chars[i] for i in range(0, len(chars))]
        self.is_valid_block = 1

    def get_data(self):
        if self.is_valid_block:
            return self.data

        return 0
