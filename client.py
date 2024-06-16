# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

import random
from server import *


class Client():
    def __init__(self, num_of_blocks, server):
        self.N = num_of_blocks
        self.server = server
        self.get_shared_key(self.server)
        self.stash = []
        self.position_map = {i: random.randint(0, 2 ** server.tree_height - 1) for i in range(num_of_blocks)}
        self.initialize_tree()

    def initialize_tree(self):
        for i in range(self.N):
            leaf = self.position_map[i]
            path = self.get_path_to_leaf(leaf)
            encrypted_data = self.encrypt(f"NULL")
            mac = self.generate_mac(encrypted_data)

            # Try to place the block in the leaf node first
            placed = False
            for bucket_id in reversed(path):
                if len(self.server.storage[bucket_id]) < self.server.bucket_size:
                    self.server.storage[bucket_id].append({'id': i, 'data': encrypted_data, 'valid': 0, 'mac': mac})
                    placed = True
                    break

            # If not placed, it will go to the stash (though this shouldn't happen during initialization)
            if not placed:
                self.stash.append({'id': i, 'data': encrypted_data, 'valid' : 0, 'mac': mac})

    def get_path_to_leaf(self, leaf):
        path = []
        idx = leaf + self.server.num_of_buckets // 2
        while idx >= 0:
            path.append(idx)
            if idx == 0:
                break
            idx = (idx - 1) // 2
        return path[::-1]

    # Reading all blocks from the path into the stash
    def read_path_to_stash(self, path):
        path_data = self.server.read_path(path)
        self.stash.extend(path_data)

    # Finding the block with block_id in the stash.
    # In case we set the new_data argument, we shall update this
    # block to contain the new data
    # The function returns the "old" data from the block
    def find_and_update_block_in_stash(self, block_id, new_data, delete):
        data = None
        block_to_remove = None
        for block in self.stash:
            if block['id'] == block_id:
                if not self.verify_mac(block['data'], block['mac']):
                    print(f"MAC verification failed for block {block_id}.")
                    return None

                data = self.decrypt(block['data'])
                if delete:
                    block['data'] = self.encrypt('NULL')
                    block['valid'] = 0
                elif new_data is not None:
                    encrypted_data = self.encrypt(new_data)
                    block['valid'] = 1
                    block['data'] = encrypted_data
                    block['mac'] = self.generate_mac(encrypted_data)
                break

        return data

    # After re-assigning blocks to the path, write the new path
    # back to the server
    def write_new_path_to_server(self, block_id, path, delete):
        # Randomize new position map encoding
        if not delete:
            # Update the position map
            new_leaf = random.randint(0, 2 ** self.server.tree_height - 1)
            self.position_map[block_id] = new_leaf

        # Write the path back to server
        # Also evict the blocks from the stash
        updated_path_data = []
        for bucket_id in path:
            bucket = [block for block in self.stash if
                      bucket_id in self.get_path_to_leaf(self.position_map[block['id']])]
            updated_path_data.append(bucket[:self.server.bucket_size])
            self.stash = [block for block in self.stash if block not in updated_path_data[-1]]

        # Write updated data with MAC
        for block in updated_path_data:
            for bucket in block:
                bucket['mac'] = self.generate_mac(bucket['data'])

        self.server.write_path(path, updated_path_data)

    # Access to server to retrieve data.
    # We pass the desired block_id and the new_data we want to update to it, if so.
    # The Function returns the read data while also updating a new path to the tree inside
    # the server. We can also delete data from a block using the "delete" argument.
    def access(self, block_id, new_data=None, delete=False):
        # Handling non-existing blocks
        if block_id not in self.position_map:
            return None

        leaf = self.position_map[block_id]
        path = self.get_path_to_leaf(leaf)

        self.read_path_to_stash(path)
        data = self.find_and_update_block_in_stash(block_id, new_data, delete)
        self.write_new_path_to_server(block_id, path, delete)

        return data

    # The client stores data associated with an ID on the server by calling:
    def store_data(self, server, id, data):
        self.access(id, new_data=data)

    # Given a name, the client retrieves associated data by calling:
    def retrieve_data(self, server, id, data):
        # the client returns None if the data does not exist.
        return self.access(id)

    # The client deletes data associated with an ID from server by calling:
    def delete_data(self, server, id, data):
        self.access(id, delete=True)

    # Get the shared key from Server
    def get_shared_key(self, server):
        self.key = self.server.share_key()

    # Encryption of a block
    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        return cipher.iv + ct_bytes

    # Decryption of a block
    def decrypt(self, enc_data):
        iv = enc_data[:AES.block_size]
        ct = enc_data[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    def generate_mac(self, data):
        h = hmac.new(self.key, data, hashlib.sha256)
        return h.digest()

    def verify_mac(self, data, mac):
        h = hmac.new(self.key, data, hashlib.sha256)
        return hmac.compare_digest(h.digest(), mac)