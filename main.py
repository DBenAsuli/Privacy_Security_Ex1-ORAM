# Advanced Topics in Online Privacy and Cybersecurity     Exercise 1
# Dvir Ben Asuli                                          318208816
# The Hebrew University of Jerusalem                      June 2024

from client import *

if __name__ == '__main__':
    #  N = input("Please enter the preferred value of N: ")
    N = 16  # FIXME REMOVE
    server = Server(num_of_blocks=N)
    client = Client(num_of_blocks=N, server=server)
