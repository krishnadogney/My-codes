"""Author: Sagar Shelke
Overall Architecture: There are two main threads. First thread sets up network initially by taking command line arguments
Second thread is to add/remove and query the status of the network.
Both threads in itself creates sub-threads and all variables changed  are global.
This program dynamically create, destroy tcp nodes in network. In this stage, following command line arguments are
supported:
* Make sure you have node.py file in the same folder as emulator.py
$ python emulator.py -h
        This will show arguments accepted by the program
-n = number of nodes in initial setup
-p = ports on which these nodes will be listening
-l = location of the node (first give all X and then all Y co-ordinates)
-seq = If number of nodes to create are very large, specifying each port is tedious.
        If you enter -seq, just enter the port where you want to start, other ports will be taken sequentially
-rloc = similar to -seq you don't need to specify all locations if number of nodes is large you just give range.
        Random locations for x and y will be selected
1. Set Up the network
for two nodes
$ python emulator.py -n 2 -p 40002 40003 -l 1 1 2 3
This will create two nodes listening on port 40002. 40003 at location (1,2) and (1,3) respectively
* Do not use port 40001 for nodes, emulation manager is listening on it for control packets
for 100 nodes
$python emulator.py -n 100 -p 40100 -l 200 -seq -rloc
This command will create 100 nodes listening on ports [40100-40199] at random location in the range 200
2. Add/ Remove nodes, Check status
Emulation manager is listening on port 40001.
a. add node
packet format
{"cmd":"add_node", "-n":2 ,"p":[40002, 40003], "-l":[1,23,13,4], "-seq":False, "-rloc": False}
This packet will make manager add 2 new nodes listening on port 40002, 40003 at location (1,13) and (23,4) respectively.
* Here we pass list(different from commandline arguments).
-seq, -rloc follows same rules. If you are specifying everything, set them to false OR
{"cmd":"add_node", "-n":10 ,"p":[40002], "-l":[100], "-seq":True, "-rloc": True}
add 10 nodes starting from 40002 at random locations.
e.g. In python you can send above packet as given below
import socket
import pickle
host = "localhost"    # everything is running on localhost
port = 40001         # manager listening on this
message = {"cmd": "add_node", "-n":4, "-p": [40009], "-l": [100], "-seq": True, "-rloc": True}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(pickle.dumps(message))  # pickle will be replaced by google protocol buffers in coming versions
s.close()
b. remove node
packet format
{"cmd":"rm_node","p":[40002, 40003]}
This packet will make manager to close nodes listening on ports 40002 and 40003
* All ports you want to close must be passed as list
You can send this packet same in python same as example given above by inserting this message
c. Query the status of the network
packet format
{"cmd":"status"}
This packet make manager tell you the current state of the network.
"""


import threading
import random
import argparse
import socket
import pickle
import node
import time
import ctrl_buf_pb2

# define dictionaries shared by all threads
port_bucket = {}   # "port":node_id
active_nodes = {}  # "port":node_object . Should be used by channel manager
threads = {}       # "port": thread_object
run_status = {}     # "port": run_status


class EmulatorHead(object):

    def __init__(self, n_nodes, node_id_list, port_numbers, location):
        self.n_nodes = n_nodes
        self.node_id_list = node_id_list
        self.port_numbers = port_numbers
        self.location = location

    def setup_nodes(self):
        """This method set-up initial network and add all parameters to global bucket"""
        global run_status

        for i in range(self.n_nodes):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                node_obj = node.Node(self.location[i], self.location[i+n_nodes], self.port_numbers[i],
                                     self.node_id_list[i], socket=s, run_status=run_status)
                port_bucket[port_numbers[i]] = self.node_id_list[i]      # to know which ports are listening
                active_nodes[self.port_numbers[i]] = node_obj     # add object to common bucket so that channel
                # manager can access it
                run_status[self.port_numbers[i]] = True
                t = threading.Thread(target=node_obj.tcp_node)
                t.start()
                threads[self.port_numbers[i]] = t        # Create thread directory to control all threads

            except:
                print("Add -seq at the end of argument to run other nodes")

    def runtime_update(self):
        """This method continuously listen for TCP packets and add/removes node from network"""
        global run_status
        global active_nodes

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 40001))
        sock.listen(1)
        print("Emulator Manager is running on port 40001. Send TCP control packets here")

        while True:
            conn, addr = sock.accept()
            print("New control command from {}".format(addr))

            data = conn.recv(1024)

            rec_control = ctrl_buf_pb2.Control()      # decode protobuf using class object
            rec_control.ParseFromString(data)
            command = rec_control.cmd
            if command == "add_node":
                nodes_to_add = rec_control.non
                is_seq_new = rec_control.seq
                rloc_new = rec_control.rloc
                node_id_list_new = random.sample(range(100), nodes_to_add)
                if is_seq_new:
                    port_numbers_new = [rec_control.ports[0] + i for i in range(nodes_to_add)]
                else:
                    port_numbers_new = rec_control.ports
                if rloc_new:
                    location_new = random.sample(range(rec_control.loc[0]), nodes_to_add * 2)
                else:
                    location_new = rec_control.loc

                for j in range(nodes_to_add):

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    node_obj = node.Node(location_new[j], location_new[j + nodes_to_add], port_numbers_new[j],
                                         node_id_list_new[j],socket=s, run_status=run_status)
                    port_bucket[port_numbers_new[j]] = node_id_list_new[j]
                    active_nodes[port_numbers_new[j]] = node_obj
                    run_status[port_numbers_new[j]] = True
                    t = threading.Thread(target=node_obj.tcp_node)
                    t.start()
                    threads[port_numbers_new[j]] = t

            elif command == "rm_node":
                port_rmt = rec_control.ports
                for port in port_rmt:
                    run_status[port] = False
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # we establish connection and close
                    # it immediately
                    s.connect(("localhost", port))
                    s.close()
                    time.sleep(1)

                    del active_nodes[port] # update all buckets
                    del port_bucket[port]
                    del run_status[port]
                    del threads[port]

            elif command == "status":
                print("Following is the current status of the network")
                for k, v in port_bucket.items():
                    print("node {} is running on port {}".format(v, k))


if __name__ == "__main__":

    # Parse the arguments given through command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, dest="nnodes", help="number of nodes you want")
    parser.add_argument("-p", nargs="+", type=int, dest="portnum", help="port number for nodes to listen. Exclude port"
                        " 40001 ")
    parser.add_argument("-l", nargs="+", type=int, dest="location", help="first enter all X and then all Y ")
    parser.add_argument("-seq", action="store_true", dest="seqp", default=False,  help="pass -seq at the end and give "
                        "only initial port. We will take other ports in sequence")
    parser.add_argument("-rloc", action="store_true", dest="rloc", default=False, help="pass -rloc to place nodes at "
                        "random location. *NOTE- pass range in -l OR default is 100")

    args = parser.parse_args()
    n_nodes = args.nnodes
    node_id_list = random.sample(range(100), n_nodes)
    is_seq = args.seqp
    if is_seq:
        port_numbers = [args.portnum[0] + i for i in range(n_nodes)]
    else:
        port_numbers = args.portnum

    # Emulation manager always listens on port 40001. If this port is entered for node, program exits
    for i in range(len(port_numbers)):
        if port_numbers[i] == 40001:
            print("You can not use 40001 as it is used by emulation manager")
            exit(1)

    if args.rloc:
        location = random.sample(range(args.location[0]), n_nodes*2)
    else:
        location = args.location

    primary_threads = []

    head_obj = EmulatorHead(n_nodes, node_id_list, port_numbers, location)

    thread = threading.Thread(target=head_obj.setup_nodes)               # set up thread
    thread.start()
    primary_threads.append(thread)
    thread = threading.Thread(target=head_obj.runtime_update)           # add/remove thread
    thread.start()
    primary_threads.append(thread)

    for thread in primary_threads:                                      # join threads to wait till all are executed
        thread.join()

