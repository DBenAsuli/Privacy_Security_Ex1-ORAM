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
        self.block_size = self.server.bucket_size
        self.position_map = {i: random.randint(0, 2 ** server.tree_height - 1) for i in range(num_of_blocks)}
        self.initialize_tree()

    # The client stores data associated with an ID on the server by calling:
    def store_data(self, server, id, data):
        self.access(id, new_data=data, server=server)

    # Given a name, the client retrieves associated data by calling:
    def retrieve_data(self, server, id, data):
        # the client returns None if the data does not exist.
        val = self.access(id, server=server)

        return val

    # The client deletes data associated with an ID from server by calling:
    def delete_data(self, server, id, data):
        self.access(id, delete=True, server=server)

    # Access to server to retrieve data.
    # We pass the desired block_id and the new_data we want to update to it, if so.
    # The Function returns the read data while also updating a new path to the tree inside
    # the server. We can also delete data from a block using the "delete" argument.
    def access(self, block_id, new_data=None, delete=False, server=None):
        if server is None:
            server = self.server
            self.key = server.share_key()
            self.initialize_tree(server=server)

        # Handling non-existing blocks
        if block_id not in self.position_map:
            return None

        leaf = self.position_map[block_id]
        path = self.get_path_to_leaf(leaf, server=server)

        self.read_path_to_stash(path, server=server)
        data = self.find_and_update_block_in_stash(block_id, new_data, delete, server=server)

        self.write_new_path_to_server(block_id, path, delete, server=server)

        # Back to default
        self.key = self.server.share_key()
        return data

    # Get the shared key from Server
    def get_shared_key(self, server):
        self.key = server.share_key()

    # Encryption of data using CTR Mode
    def encrypt(self, plaintext):
        plaintext = plaintext.ljust(self.block_size).encode('utf-8')  # Ensure plaintext is bytes and block size
        nonce = get_random_bytes(8)  # 8-byte nonce
        ctr = Counter.new(64, prefix=nonce)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        ciphertext = cipher.encrypt(plaintext)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    # Decryption of data
    def decrypt(self, encrypted_block):
        encrypted_data = base64.b64decode(encrypted_block)
        nonce = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        ctr = Counter.new(64, prefix=nonce)
        cipher = AES.new(self.key, AES.MODE_CTR, counter=ctr)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8').rstrip()

    # Generate MAC for authentication
    def generate_mac(self, data):
        key_bytes = self.key if isinstance(self.key, bytes) else self.key.encode()
        h = hmac.new(key_bytes, data.encode(), hashlib.sha256)
        return h.digest()

    # Given data, performs MAC authentication
    def verify_mac(self, data, mac):
        key_bytes = self.key if isinstance(self.key, bytes) else self.key.encode()
        h = hmac.new(key_bytes, data.encode(), hashlib.sha256)
        return hmac.compare_digest(h.digest(), mac)

    # initialize the Storage for the Server
    def initialize_tree(self, server=None):
        if server is None:
            server = self.server
            self.key = server.share_key()

        for i in range(self.N):
            leaf = self.position_map[i]
            path = self.get_path_to_leaf(leaf, server)
            encrypted_data = self.encrypt(f"NULL")
            mac = self.generate_mac(encrypted_data)

            # Try to place the block in the leaf node first
            placed = False
            for bucket_id in reversed(path):
                if server.get_bucket_size(bucket_id) < server.bucket_size:
                    server.add_to_bucket(bucket_id, {'id': i, 'data': encrypted_data, 'valid': 0, 'mac': mac})
                    placed = True
                    break

            # If not placed, it will go to the stash (though this shouldn't happen during initialization)
            if not placed:
                self.stash.append({'id': i, 'data': encrypted_data, 'valid': 0, 'mac': mac})

    # Fine the indexes path inside a binary tree on a way to a leaf
    # To use on storage inside the server
    def get_path_to_leaf(self, leaf, server):
        path = []
        idx = leaf + server.num_of_buckets // 2
        while idx >= 0:
            path.append(idx)
            if idx == 0:
                break
            idx = (idx - 1) // 2
        return path[::-1]

    # Reading all blocks from the path into the stash
    def read_path_to_stash(self, path, server):
        path_data = server.read_path(path)
        self.stash.extend(path_data)

    # Finding the block with block_id in the stash.
    # In case we set the new_data argument, we shall update this
    # block to contain the new data
    # The function returns the "old" data from the block
    def find_and_update_block_in_stash(self, block_id, new_data, delete, server):
        data = None

        for block in self.stash:
            if block['id'] == block_id:

                # Authenticity check
                if not self.verify_mac(block['data'], block['mac']):
                    print(f"MAC verification failed for block {block_id}.")
                    return None

                data = self.decrypt(block['data'])
                if delete:
                    # If we wish to delete the data in this block, we will return the data to "NULL"
                    block['data'] = self.encrypt('NULL')
                    block['valid'] = 0
                elif new_data is not None:
                    # If we wish to update the data in this block, we will change the data to to the desired value
                    encrypted_data = self.encrypt(new_data)
                    block['valid'] = 1
                    block['data'] = encrypted_data
                    block['mac'] = self.generate_mac(encrypted_data)
                break
        return data

    # After re-assigning blocks to the path, write the new path
    # back to the server
    def write_new_path_to_server(self, block_id, path, delete, server):

        # Randomize new position map encoding
        if not delete:
            new_leaf = random.randint(0, 2 ** server.tree_height - 1)
            self.position_map[block_id] = new_leaf

        updated_path_data = []

        # Iterate through each bucket ID in the path from the root to the leaf node.
        for bucket_id in path:
            # For each Bucket ID along the path,
            # select blocks from the stash that should be placed in this bucket:
            # For each block inside the stash,
            # Check if the current bucket ID is part of the path from root to the block.
            # If so, add it do the updated data path.
            bucket = [block for block in self.stash if
                      bucket_id in self.get_path_to_leaf(self.position_map[block['id']], server)]
            updated_path_data.append(bucket[:server.bucket_size])

            # Evict the relevant blocks from the stash
            self.stash = [block for block in self.stash if block not in updated_path_data[-1]]

        # Write updated data with MAC
        for block in updated_path_data:
            for bucket in block:
                bucket['mac'] = self.generate_mac(bucket['data'])

        # Write the new updated path back to server
        server.write_path(path, updated_path_data)
