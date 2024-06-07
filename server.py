# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

import Crypto.Cipher
from collections import OrderedDict

DATA_LEN = 4

class Server():
    N = 0
    datablocks = dict()

    def __init__(self, num_of_blocks):
        self.N = num_of_blocks

    def store_data(self, id, data):
        pass

    def retrieve_data(self, id, data):
        pass

    def delete_data (self, id, data):
        pass

    def new_user(self, id):
        self.datablocks[id] = []

        for i in range(0, self.N):
            new_datablock = DataBlock()
            self.datablocks[id].append(new_datablock)

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

