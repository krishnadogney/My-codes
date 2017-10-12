"""Author: Sagar Shelke
This is a Node class. Each node is an object of this class with its own namespace.

Each node continuously check for what its running status should be in run_status{} dictionary. When status is False,
it closes the connection ."""

import pickle
import socket


class Node(object):

    def __init__(self, x, y, port, node_id, socket, run_status):
        self.socket = socket
        self.x = x
        self.y = y
        self.port = port
        self.node_id = node_id
        self.flag = False
        self.buffer = 0
        self.run_status = run_status

    def tcp_node(self):
        host = "localhost"
        port = self.port
        self.socket.bind((host, port))
        self.socket.listen(1)
        print("node {} running on port {} at location {},{} waiting for connection".format(self.node_id, port, self.x, self.y))
        while True:
            conn, addr = self.socket.accept()
            print('Connected by {} on port {}'.format(addr, conn))
            data = conn.recv(1024)
            if len(data) > 0:
                packet = pickle.loads(data)
                no_of_packets = packet["no of packet"]
                self.buffer = self.buffer + no_of_packets
                self.flag = True
                print("new packet received. Now buffer ={} at node {}".format(self.buffer, self.node_id))

            if not self.run_status[self.port]:
                break
        print("node {} running at port {} is closing".format(self.node_id, self.port))
        conn.close()
