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
-d = number of ports used for data transfer
-vc = number of ports used for voice transfer
-vd = number of ports used for video transfer.

NOTE* video and voice nodes are given starting slot such that number of slots allocated are more than data nodes. This
is true for both initial set-up and newly added nodes.

1. Set Up the network
for two nodes
$ python emulator.py -n 2 -p 40002 40003 -l 1 1 2 3 -d 1 -vc 1 -vd 0
This will create two nodes listening on port 40002. 40003 at location (1,2) and (1,3) respectively
* Port emulation manager is listening on is taken from config file. If you enter node port same as emulation manager,
program exits

$python emulator.py -n 100 -p 40100 -l 200 -seq -rloc -d 50 -vc 25 -vd 25
This command will create 100 nodes listening on ports [40100-40199] at random location in the range 200

2. Add/ Remove nodes, Check status
Check port on which emulation manager is running from config file.

a. add node
packet format
We use protocol buffers to send data since they are language and platform neutral.  

cmd = "add_node", non = 2 ,ports = [40002, 40003], loc = [1,23,13,4], seq = False, rloc = False

This packet will make manager add 2 new nodes listening on port 40002, 40003 at location (1,13) and (23,4) respectively.
* Here we pass list(different from commandline arguments).
seq, rloc follows same rules. If you are specifying everything, set them to false OR
cmd = "add_node", non = 10 ,ports = [40002], loc = [100], seq = True, rloc = True}
add 10 nodes starting from 40002 at random locations.

* CHECK control_client.py file to learn how to code protocol buffers

b. remove node
packet format
cmd = "rm_node",ports = [40002, 40003]
This packet will make manager to close nodes listening on ports 40002 and 40003
* All ports you want to close must be passed as list
You can send this packet same in python same as example given above by inserting this message

c. Query the status of the network
packet format
cmd = "status"
This packet make manager tell you the current state of the network.

sample_data_generator.py is the file generating data for nodes.
"""


import threading
import random
import argparse
import socket
import node
import operator
import time
import ctrl_buf_pb2
import json


# define dictionaries shared by all threads
port_bucket = {}   # "port":node_id
active_nodes = {}  # "port":node_object . Should be used by channel manager
threads = {}       # "port": thread_object
run_status = {}     # "port": run_status
group_node_object_dict = {}
group_node_id_dict = {}
sender_receiver = {}
number_of_groups = 3
node_object_global_list = []
node_id_global_list = []
node_start_slot_global_list = []
slot_assignment_list = []
data_req_of_nodes = {}
poll = []
timer_flag = []


class EmulatorHead(object):

    def __init__(self, n_nodes, node_id_list, port_numbers, location, data_nodes, voice_nodes, video_nodes, em_port,
                 slot_len):
        self.n_nodes = n_nodes
        self.node_id_list = node_id_list
        self.port_numbers = port_numbers
        self.location = location
        self.data_nodes = data_nodes                # A list containing ports for data nodes
        self.voice_nodes = voice_nodes              # A list containing ports for voice nodes
        self.video_nodes = video_nodes              # A list containing ports for video nodes
        self.emulation_port = em_port
        self.slot_len = slot_len
        self.starting_slot_numbers_not_used = []    # list to keep track of starting slot numbers which are un-allocated
        self.slot_slot_length_dict = {}             # key = starting slot, value = slot length

    def slot_alloc(self, num_slots):
        """this function gives schedule for a frame.This function can be called at the starting of ech frame or same
        schedule can be used for all the frames.
        Arguments
        ----------
        num_slots : number of slots in a frame

        Returns
        --------
        dictionary where key is starting slot number and value is number of slots.
        """
        initial = 2
        prime_num = []
        slot_slot_len_dict = {}
        for number in range(initial + 1, num_slots + 1):
            count = 0
            for div in range(initial, number):
                if (number % div) == 0:
                    count = count + 1
            if count < 1:
                prime_num.append(number)
        for ind, item in enumerate(prime_num):
            if ind < len(prime_num) - 1:
                slot_slot_len_dict[item] = prime_num[ind + 1] - prime_num[ind]
            elif ind == len(prime_num) - 1:
                slot_slot_len_dict[item] = num_slots - prime_num[ind]
        slot_slot_len_dict[1] = 2

        return slot_slot_len_dict

    def setup_nodes(self):
        """This method set-up initial network and add all parameters to global bucket.
        """
        global run_status
        global group_node_object_dict
        global sender_receiver
        global node_object_global_list
        global node_id_global_list
        global slot_assignment_list

        self.slot_slot_length_dict = self.slot_alloc(self.slot_len)   # key= starting slot, value= slot length

        sorted_list_of_tuples = sorted(self.slot_slot_length_dict.items(), key=operator.itemgetter(1))

        for key_value in sorted_list_of_tuples:
            self.starting_slot_numbers_not_used.append(key_value[0])

        # crete lists for data, voice and video nodes
        if self.data_nodes:
            list_for_data_nodes = sorted_list_of_tuples[0:len(self.data_nodes)]

        if self.voice_nodes:
            list_for_voice_nodes = sorted_list_of_tuples[len(self.data_nodes): len(self.data_nodes) +
                                                         len(self.voice_nodes)]

        if self.video_nodes:
            list_for_video_nodes = sorted_list_of_tuples[-len(self.video_nodes):]

        index_data = 0
        index_voice = 0
        index_video = 0

        for i in range(self.n_nodes):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # select starting slot and number of sl;ots for each object
                if self.port_numbers[i] in self.data_nodes:
                    start_slot = list_for_data_nodes[index_data][0]
                    num_of_slots = list_for_data_nodes[index_data][1]
                    index_data += 1

                elif self.port_numbers[i] in self.voice_nodes:
                    start_slot = list_for_voice_nodes[index_voice][0]
                    num_of_slots = list_for_voice_nodes[index_voice][1]
                    index_voice += 1

                else:
                    start_slot = list_for_video_nodes[index_video][0]
                    num_of_slots = list_for_video_nodes[index_video][1]
                    index_video += 1

                # update slot assignment and un-assigned lists
                slot_assignment_list.append(start_slot)
                self.starting_slot_numbers_not_used.remove(start_slot)

                node_obj = node.Node(self.location[i], self.location[i+n_nodes], self.port_numbers[i],
                                     self.node_id_list[i], socket=s, run_status=run_status, start_slot=start_slot,
                                     num_slots=num_of_slots)

                port_bucket[port_numbers[i]] = self.node_id_list[i]      # to know which ports are listening
                active_nodes[self.port_numbers[i]] = node_obj          # add object to common bucket for channel manager

                # add newly created node into group
                group = random.randrange(1, number_of_groups + 1)
                group_node_object_dict[group].append(node_obj)
                group_node_id_dict[group].append(self.node_id_list[i])

                node_object_global_list.append(node_obj)                # append node object in global list
                node_id_global_list.append(self.node_id_list[i])
                node_start_slot_global_list.append(start_slot)

                run_status[self.port_numbers[i]] = True               # Run status is used for removing the node
                t = threading.Thread(target=node_obj.tcp_node)
                t.start()
                threads[self.port_numbers[i]] = t                     # Create thread directory to control all threads
            except:
                print("Add -seq at the end of argument to run other nodes")
                raise

        # select random receiver for each node generated
        for index, value in enumerate(node_object_global_list):

            temp = node_object_global_list.pop(index)
            random_receiver = random.randrange(0, len(node_object_global_list))
            sender_receiver[temp] = node_object_global_list[random_receiver]
            node_object_global_list.insert(index, temp)

    def runtime_update(self):
        """This method continuously listen for TCP packets and add/removes node from network.
        """
        global run_status
        global active_nodes

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", self.emulation_port))
        sock.listen(1)
        print("Emulator Manager is running on port {}. Send TCP control packets here".format(self.emulation_port))

        while True:
            conn, addr = sock.accept()
            print("New control command from {}".format(addr))

            data = conn.recv(1024)

            rec_control = ctrl_buf_pb2.Control()      # decode proto-buf using class object
            rec_control.ParseFromString(data)
            command = rec_control.cmd
            if command == "add_node":
                nodes_to_add = rec_control.non
                is_seq_new = rec_control.seq
                rloc_new = rec_control.rloc
                dn_new = rec_control.dn
                vcn_new = rec_control.vcn
                vdn_new = rec_control.vdn
                grouping_new = rec_control.group     # check control_client.py file details of arguments

                node_id_list_new = list(range(self.n_nodes+1, self.n_nodes + nodes_to_add + 1))  # create new node ID's
                # these are sequential to original set-up network

                if is_seq_new:
                    port_numbers_new = [rec_control.ports[0] + i for i in range(nodes_to_add)]
                else:
                    port_numbers_new = rec_control.ports                   # assign port numbers

                if rloc_new:
                    location_new = random.sample(range(rec_control.loc[0]), nodes_to_add * 2)
                else:
                    location_new = rec_control.loc                        # Create random locations

                temp_dict_port_group = {}     # key = port number , value= group it belongs to

                last = 0          # Fill above dictionary which is used to assign groups to new nodes
                index = 0
                for i in range(number_of_groups):
                    for j in range(last, last + grouping_new[i]):
                        temp_dict_port_group[port_numbers_new[j]] = i + 1
                        index += 1
                    last = index

                for j in range(nodes_to_add):

                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    # Firs assign slots to data nodes, then voice and at the end video
                    if dn_new:
                        start_slot = self.starting_slot_numbers_not_used[j]
                        num_of_slots = self.slot_slot_length_dict[start_slot]
                        dn_new = dn_new - 1

                    if vcn_new:
                        if dn_new:
                            pass
                        else:
                            start_slot = self.starting_slot_numbers_not_used[j]
                            num_of_slots = self.slot_slot_length_dict[start_slot]
                            vcn_new = vcn_new - 1

                    if vdn_new:
                        if dn_new or vdn_new:
                            pass
                        else:
                            start_slot = self.starting_slot_numbers_not_used[(len(self.starting_slot_numbers_not_used) - 1) -j]
                            num_of_slots = self.slot_slot_length_dict[start_slot]
                            vdn_new = vdn_new - 1

                    # Update slot assignment and un-assigned list
                    slot_assignment_list.append(start_slot)
                    self.starting_slot_numbers_not_used.remove(start_slot)

                    node_obj = node.Node(location_new[j], location_new[j + nodes_to_add], port_numbers_new[j],
                                         node_id_list_new[j], socket=s, run_status=run_status, start_slot=start_slot,
                                         num_slots=num_of_slots)

                    port_bucket[port_numbers_new[j]] = node_id_list_new[j]
                    active_nodes[port_numbers_new[j]] = node_obj

                    # assign groups
                    group = temp_dict_port_group[port_numbers_new[j]]
                    group_node_object_dict[group].append(node_obj)
                    group_node_id_dict[group].append(self.node_id_list[j])

                    node_object_global_list.append(node_obj)     # Update global buckets
                    node_id_global_list.append(self.node_id_list[j])
                    node_start_slot_global_list.append(start_slot)

                    run_status[port_numbers_new[j]] = True
                    t = threading.Thread(target=node_obj.tcp_node)
                    t.start()
                    threads[port_numbers_new[j]] = t

            elif command == "rm_node":
                port_rmt = rec_control.ports
                for port in port_rmt:
                    run_status[port] = False
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # we establish connection and close
                    s.connect(("localhost", port))
                    s.close()
                    time.sleep(1)

                    del active_nodes[port]                                   # update all buckets
                    del port_bucket[port]
                    del run_status[port]
                    del threads[port]

            elif command == "status":
                print("Following is the current status of the network")
                for k, v in port_bucket.items():
                    print("node {} is running on port {}".format(v, k))
                print("-------------------------------")
                print("Currently {} groups are created.".format(number_of_groups))
                for k, v in group_node_id_dict.items():
                    print("group {} contains nodes {} ".format(k, v))
                print("--------------------------------")


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
    parser.add_argument("-d", type=int, dest="data_app", help="number of nodes for data application")
    parser.add_argument("-vc", type=int, dest="voice_app", help="number of nodes for voice application")
    parser.add_argument("-vd", type=int, dest="video_app", help="number of nodes for video application")

    args = parser.parse_args()

    n_nodes = args.nnodes

    num_data_nodes = args.data_app
    num_voice_nodes = args.voice_app
    num_video_nodes = args.video_app

    data_nodes_list = []
    voice_nodes_list = []
    video_nodes_list = []

    # Sanity check for user input
    total = num_data_nodes + num_voice_nodes + num_video_nodes
    if total == n_nodes:
        pass
    else:
        print("Node calculations went wrong!")
        exit(1)

    node_id_list = list(range(1, n_nodes+1))          # generating sequential ID's
    is_seq = args.seqp

    if is_seq:
        port_numbers = [args.portnum[0] + i for i in range(n_nodes)]   # create sequential port numbers
    else:
        port_numbers = args.portnum

    with open("./prog_config.json", "r") as f:                 # Read configuration file to fetch hyper-parameters
        config = json.load(f)

    emulator_port = config["EM"]["PORT"]
    num_slots = config["CM"]["SLOTS"]
    slot_length = config["CM"]["SLOT_LENGTH"]

    # If port of emulation manager is entered for node, program exits
    if emulator_port in port_numbers:
        print("You can not use {} as it is used by emulation manager".format(emulator_port))
        exit(1)

    # Separating data, voice and video applications node
    if num_data_nodes:
        data_nodes_list = port_numbers[0:num_data_nodes]
    if num_voice_nodes:
        voice_nodes_list = port_numbers[num_data_nodes: num_data_nodes + num_voice_nodes]
    if num_video_nodes:
        video_nodes_list = port_numbers[num_data_nodes + num_voice_nodes: num_data_nodes + num_voice_nodes +
                                        num_video_nodes]

    if args.rloc:
        location = random.sample(range(args.location[0]), n_nodes*2)    # Generate random locations
    else:
        location = args.location

    for i in range(1, number_of_groups + 1):
        group_node_object_dict[i] = []          # Empty dictionary key= group number , value = node_objects_in group
        group_node_id_dict[i] = []              # Empty dictionary key= group number , value = node_object_in group

    primary_threads = []

    head_obj = EmulatorHead(n_nodes, node_id_list, port_numbers, location, data_nodes_list,
                            voice_nodes_list, video_nodes_list, emulator_port, num_slots)

    thread = threading.Thread(target=head_obj.setup_nodes)               # set up thread
    thread.start()
    time.sleep(1)

    primary_threads.append(thread)
    thread = threading.Thread(target=head_obj.runtime_update)           # add/remove thread
    thread.start()
    primary_threads.append(thread)

    for thread in primary_threads:                                      # join threads to wait till all are executed
        thread.join()


