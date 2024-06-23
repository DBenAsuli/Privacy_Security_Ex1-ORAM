# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

import time
import random
import threading
from client import *
from queue import Queue
import matplotlib.pyplot as plt


def benchmark_throughput(num_blocks_list, num_requests):
    throughput_results = []

    for num_blocks in num_blocks_list:
        server = Server(num_of_blocks=num_blocks)
        client = Client(server=server)

        # Preload the server with data
        for i in range(num_blocks):
            client.access(i, f"d{i}")

        start_time = time.time()
        for _ in range(num_requests):
            block_id = random.randint(0, num_blocks - 1)
            client.access(block_id)

        end_time = time.time()
        throughput = num_requests / (end_time - start_time)
        throughput_results.append([num_blocks, throughput])
        print(f"Throughput for N={num_blocks}: {throughput:.2f} requests/sec")

    return throughput_results


def benchmark_latency(num_blocks, num_requests, max_threads):
    server = Server(num_of_blocks=num_blocks)
    client = Client(server=server)

    latency_results = []

    # Preload the server with data
    for i in range(num_blocks):
        client.access(i, f"d{i}")

    results = Queue()

    def worker():
        for _ in range(num_requests):
            block_id = random.randint(0, num_blocks - 1)
            start_time = time.time()
            client.access(block_id)
            end_time = time.time()
            results.put(end_time - start_time)

    for num_threads in range(1, max_threads + 1):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total_latency = 0
        for _ in range(results.qsize()):
            total_latency += results.get()

        avg_latency = total_latency / (num_requests * num_threads)
        latency_results.append([num_threads, avg_latency])
        print(f"Average latency with {num_threads} threads: {avg_latency:.6f} seconds/request")

    return latency_results


def plot_throughput(throughput_results):
    num_blocks = [result[0] for result in throughput_results[0]]
    throughputs = throughput_results[1]

    plt.figure(figsize=(10, 6))
    plt.plot(num_blocks, throughputs, marker='o')
    plt.title('Throughput vs. Database Size')
    plt.xlabel('Database Size (N)')
    plt.ylabel('Throughput (requests/sec)')
    plt.grid(True)
    plt.show()


def plot_latency(latency_results):
    num_threads = [result[0] for result in latency_results[0]]
    latencies = latency_results[1]

    plt.figure(figsize=(10, 6))
    plt.plot(num_threads, latencies, marker='o')
    plt.title('Latency vs. Throughput')
    plt.xlabel('Number of Threads (Simulated Throughput)')
    plt.ylabel('Average Latency (seconds/request)')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    num_blocks_list = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2056]
    num_requests = 250
    num_of_iterations = 10
    throughput_results = []
    latency_results = []

    print("Benchmarking Throughput:")
    for _ in range(num_of_iterations):
        print("\nIteration: " + str(_) + "\n")
        throughput_results.append(benchmark_throughput(num_blocks_list, num_requests))

    throughput_results_average = []
    for i in range(len(throughput_results[0])):
        avg = sum(arr[i][1] for arr in throughput_results) / len(throughput_results)
        throughput_results_average.append(avg)

    plot_throughput([throughput_results[0], throughput_results_average])

    print("\nBenchmarking Latency:")
    num_blocks = 64
    num_requests = 1000
    max_threads = 25

    for _ in range(num_of_iterations):
        print("\nIteration: " + str(_) + "\n")
        latency_results.append(benchmark_latency(num_blocks, num_requests, max_threads))

    latency_results_average = []

    for i in range(len(latency_results[0])):
        avg = sum(arr[i][1] for arr in latency_results) / len(latency_results)
        latency_results_average.append(avg)

    plot_latency([latency_results[0], latency_results_average])

    print("\nDone!")
