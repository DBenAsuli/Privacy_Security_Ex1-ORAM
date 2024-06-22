from main import *

verbosity = "HIGH" # Change if you don't want a lot of prints

if __name__ == '__main__':
    error = 0
    num_of_tests = random.randint(10, 100)
    print("Starting tests... \n")
    print("Performing " + str(num_of_tests) + " tests: \n")

    for k in range(num_of_tests):
        num_of_blocks = random.randint(2, 1000)

        if verbosity == "HIGH":
            print("Performing test " + str(k) + " with " + str(num_of_blocks) + " blocks")

        server = Server(num_of_blocks=num_of_blocks)
        client = Client(server=server, num_of_blocks=num_of_blocks)

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

        if verbosity == "HIGH":
            if error == 0:
                print("test " + str(k) + " PASSED \n")
            else:
                print("test " + str(k) + " FAILED \n")
                break

    if error == 0:
        print("All " + str(num_of_tests) + " tests PASSED")
    else:
        print("Some tests FAILED")
