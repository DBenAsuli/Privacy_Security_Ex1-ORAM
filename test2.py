from main import *

if __name__ == '__main__':
    server = Server(num_of_blocks=16)
    client = Client(server=server, num_of_blocks=16)

    # Access data from blocks
    print("\nAccessing data...")
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        print(f"Block {i}: {data}")

    # Write data to blocks
    print("Writing data...")
    for i in range(16):
        client.store_data(server, i, f"dat{i:X}")

    # Access data from blocks
    print("\nAccessing data...")
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        print(f"Block {i}: {data}")

    # Update a block and read it back
    print("\nUpdating block 1...")
    client.store_data(server,1, "udat")
    data = client.retrieve_data(server, 1, "")
    print(f"Block 1: {data}")

    # Remove a block
    print("\nRemoving block 2...")
    client.delete_data(server, 2, "")
    data = client.retrieve_data(server, 2, "")
    print(f"Block 2: {data}")  # Should return None as block 2 has been removed

    # Update a block and read it back
    print("\nUpdating block 2...")
    client.store_data(server,2, "udat")
    data = client.retrieve_data(server, 2, "")
    print(f"Block 2: {data}")

    # Accessing a non-existent block (beyond initial blocks)
    print("\nAccessing a non-existent block (id 17)...")
    data = client.retrieve_data(server,17, "")
    print(f"Block 17: {data}")  # Should return None as block 17 does not exist
