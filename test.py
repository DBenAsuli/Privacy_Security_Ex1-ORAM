from main import *

if __name__ == '__main__':
    num_of_blocks = 2000
    server = Server(num_of_blocks=num_of_blocks)
    client = Client(server=server, num_of_blocks=num_of_blocks)
    error = 0

    print("Starting test...\n")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")

        if data != "NULL":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: \"NULL\"\n")
            error = 1

    # Write data to blocks
    for i in range(16):
        client.store_data(server, i, f"dat{i:X}")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if data != f"dat{i:X}":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: dat{i:X}\n")
            error = 1

    # Update a block and read it back
    for i in range(16):
        client.store_data(server, i, f"uda{i:X}")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if data != f"uda{i:X}":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: uda{i:X}\n")
            error = 1

    # Remove a block
    for i in range(16):
        client.delete_data(server, i, "")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if data != "NULL":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: \"NULL\"\n")
            error = 1

    # Update a block and read it back
    for i in range(16):
        client.store_data(server, i, f"udb{i:X}")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if data != f"udb{i:X}":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: udb{i:X}\n")
            error = 1

    # Update a block and read it back
    for i in range(16):
        if i % 2:
            client.store_data(server, i, f"udc{i:X}")
        else:
            client.store_data(server, i, f"udd{i:X}")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if i % 2:
            if data != f"udc{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: udc{i:X}\n")
                error = 1
        else:
            if data != f"udd{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: udd{i:X}\n")
                error = 1

    # Remove a block
    for i in range(16):
        if i % 2:
            client.delete_data(server, i, "")

        # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if i % 2:
            if data != f"NULL":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: \"NULL\"\n")
                error = 1
        else:
            if data != f"udd{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: udd{i:X}\n")
                error = 1

    # Remove a block
    for i in range(16):
        if i % 2 == 0:
            client.delete_data(server, i, "")

    # Update a block and read it back
    for i in range(16):
        client.store_data(server, i, f"ude{i:X}")

    # Access data from blocks
    for i in range(16):
        data = client.retrieve_data(server, i, "")
        if data != f"ude{i:X}":
            print("FAIL")
            print(f"Block {i}: {data}")
            print(f"Supposed to be: ude{i:X}\n")
            error = 1

    # Accessing a non-existent block (beyond initial blocks)
    data = client.retrieve_data(server, num_of_blocks + 1, "")
    if data != None:
        print("FAIL")
        print(f"Block {num_of_blocks + 1}: {data}")
        print(f"Supposed to be: None\n")
        error = 1

    if error == 0:
        print("All tests PASSED")
    else:
        print("Some tests FAILED")
