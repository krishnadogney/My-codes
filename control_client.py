"""Author: Sagar Shelke
This is a client program which sends control packets emulation manager.
Here we are using google protocol buffers to serialize data since they are language neutral.
ctrl_buf.proto is protocol file with data structure we want to serialize.

To install protobuf compiler on ubuntu
sudo apt-get install protobuf-compiler

To compile .proto file in linux
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/ctrl_buf.proto

e.g. consider you are in the same folder as that of .proto file
protoc -I=./ --python_out=./ ./ctrl_buf.proto

This gives ctrl_buf_pb2.py file in the same directory.
"""

import socket
import ctrl_buf_pb2

emulator_manager_port = 40001
emulator_manager_ip = "localhost"


def send_pkt(cmd, non, ports, loc, seq, rloc, dn, vcn, vdn, group):
    """This function creates socket and send a packet serialized using protocol buffer
    Arguments
    ---------
    cmd: string command
        currently one of the "add_node","rm_node","status"
    non: number of nodes to add
    ports: a port list
    loc : location list
    seq : a boolean True or False
         if True, only one port is given and other are taken in sequence
    rloc: a boolean True or False
        if True, range of location is passed instead of passing individual x,y
    dn : number of data nodes out of total nodes you want to add
    vcn: number of voice nodes out of total nodes you want to add
    vdn: number of video nodes out of total nodes you want to add
    group: array with elements equal to number of groups
           e.g. there are three groups and you want to add six nodes
           group([3,2,1])
           Above argument means, add first three ports from ports argument into group 1, next 2 into group 2
           and last one into group 3
           NOTE* Ports are always taken sequentially

    NOTE* Here non = dn + vcn + vdn

    dn, cvn and vdn are compulsory parameters when you are adding node

    """

    # Two sanity checks on user input
    if dn + vcn + vdn != non:
        print("Number of nodes does not match dn, vcn and vdn!")
        exit(1)

    if sum(group) != non:
        print("Number of nodes in group attribute are more or less than total number of nodes")
        exit(1)

    host = emulator_manager_ip
    port_manager = emulator_manager_port

    control = ctrl_buf_pb2.Control()    # create an object of compiled class

    control.cmd = cmd                  # adding elements to proto-buf packet
    control.non = non
    control.ports.extend(ports)
    control.loc.extend(loc)
    control.seq = seq
    control.rloc = rloc
    control.dn = dn
    control.vcn = vcn
    control.vdn = vdn
    control.group.extend(group)

    data = control.SerializeToString()     # Serialized string

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        # create socket and send data
    s.connect((host, port_manager))
    s.sendall(data)
    s.close()


if __name__ == "__main__":
    """You can always check status first and then make decisions about adding/ removing nodes.
    """
    cmd_pass = "status"
    non_pass = 1
    ports_pass = [40009]
    loc_pass = [10, 10]
    seq_pass = False
    rloc_pass = False
    dn_pass = 1
    vcn_pass = 0
    vdn_pass = 0
    group_pass = [1, 0, 0]

    send_pkt(cmd_pass, non_pass, ports_pass, loc_pass, seq_pass, rloc_pass, dn_pass, vcn_pass, vdn_pass, group_pass)
