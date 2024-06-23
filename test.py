import re
from main import *

verbosity = "HIGH"  # Change to 'HIGH' if you want more of prints

if __name__ == '__main__':
    error = 0
    num_of_tests = random.randint(10, 100)
    print("Starting tests... \n")
    print("Performing " + str(num_of_tests) + " tests: \n")

    for k in range(num_of_tests):
        num_of_blocks = random.randint(2, 1000)

        if verbosity == "HIGH":
            print("Performing test " + str(k + 1) + " with " + str(num_of_blocks) + " blocks")

        server = Server(num_of_blocks=num_of_blocks)
        client = Client(server=server)

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")

            if data != "NULL":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: \"NULL\"\n")
                error = 1

        # Write data to blocks
        for i in range(num_of_blocks):
            client.store_data(server, i, f"a{i:X}")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if data != f"a{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: a{i:X}\n")
                error = 1

        # Update a block and read it back
        for i in range(num_of_blocks):
            client.store_data(server, i, f"a{i:X}")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if data != f"a{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: a{i:X}\n")
                error = 1

        # Remove a block
        for i in range(num_of_blocks):
            client.delete_data(server, i, "")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if data != "NULL":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: \"NULL\"\n")
                error = 1

        # Update a block and read it back
        for i in range(num_of_blocks):
            client.store_data(server, i, f"b{i:X}")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if data != f"b{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: b{i:X}\n")
                error = 1

        # Update a block and read it back
        for i in range(num_of_blocks):
            if i % 2:
                client.store_data(server, i, f"c{i:X}")
            else:
                client.store_data(server, i, f"d{i:X}")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if i % 2:
                if data != f"c{i:X}":
                    print("FAIL")
                    print(f"Block {i}: {data}")
                    print(f"Supposed to be: c{i:X}\n")
                    error = 1
            else:
                if data != f"d{i:X}":
                    print("FAIL")
                    print(f"Block {i}: {data}")
                    print(f"Supposed to be: d{i:X}\n")
                    error = 1

        # Remove a block
        for i in range(num_of_blocks):
            if i % 2:
                client.delete_data(server, i, "")

            # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if i % 2:
                if data != f"NULL":
                    print("FAIL")
                    print(f"Block {i}: {data}")
                    print(f"Supposed to be: \"NULL\"\n")
                    error = 1
            else:
                if data != f"d{i:X}":
                    print("FAIL")
                    print(f"Block {i}: {data}")
                    print(f"Supposed to be: d{i:X}\n")
                    error = 1

        # Remove a block
        for i in range(num_of_blocks):
            if i % 2 == 0:
                client.delete_data(server, i, "")

        # Update a block and read it back
        for i in range(num_of_blocks):
            client.store_data(server, i, f"e{i:X}")

        # Access data from blocks
        for i in range(num_of_blocks):
            data = client.retrieve_data(server, i, "")
            if data != f"e{i:X}":
                print("FAIL")
                print(f"Block {i}: {data}")
                print(f"Supposed to be: e{i:X}\n")
                error = 1

        # Accessing a non-existent block (beyond initial blocks)
        data = client.retrieve_data(server, num_of_blocks + 1, "")
        if data != None:
            print("FAIL")
            print(f"Block {num_of_blocks + 1}: {data}")
            print(f"Supposed to be: None\n")
            error = 1

        corrupted_block = random.randint(0, num_of_blocks - 1)

        # Corrupt the data for a block directly on the server
        leaf = client.position_map[corrupted_block]
        path = client.get_path_to_leaf(leaf, server)
        path_data = server.read_path(path)

        # Find and corrupt the data block
        for block in path_data:
            if block['id'] == corrupted_block:
                block['data'] = client.encrypt("HAHA")
                break

        server.write_path(path, [path_data])
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the function that prints something
        retrieved_data = client.retrieve_data(server, corrupted_block, "")

        # Get the printed output
        printed_output = captured_output.getvalue()
        sys.stdout = sys.__stdout__

        # Check if the target regex pattern matches in the printed output
        if not re.search(r'MAC verification failed for block.*', printed_output):
            data = client.retrieve_data(server, corrupted_block, "")
            if data == "HAHA":  # Data was indeed successfully corrupted
                error = 1
                print("Data integrity corruption not caught for block " + str(corrupted_block))

        if verbosity == "HIGH":
            if error == 0:
                print("test " + str(k + 1) + " PASSED \n")
            else:
                print("test " + str(k + 1) + " FAILED \n")
                break

    if error == 0:
        print("All " + str(num_of_tests) + " tests PASSED")
    else:
        print("Some tests FAILED")
