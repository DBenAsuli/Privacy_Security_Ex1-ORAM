# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

from main import *

if __name__ == '__main__':
    server = Server(num_of_blocks=16)
    client = Client(server=server, num_of_blocks=16)

    # Write data to blocks
    print("Writing data...")
    for i in range(16):
        client.access(i, f"dat{i}")

    # Access data from blocks
    print("\nAccessing data...")
    for i in range(16):
        data = client.access(i)
        print(f"Block {i}: {data}")

    # Update a block and read it back
    print("\nUpdating block 1...")
    client.access(1, "udat")
    data = client.access(1)
    print(f"Block 1: {data}")

    # Remove a block
    print("\nRemoving block 2...")
    client.access(2, delete=True)
    data = client.access(2)
    print(f"Block 2: {data}")  # Should return None as block 2 has been removed

    # Accessing a non-existent block (beyond initial blocks)
    print("\nAccessing a non-existent block (id 17)...")
    data = client.access(17)
    print(f"Block 17: {data}")  # Should return None as block 17 does not exist
