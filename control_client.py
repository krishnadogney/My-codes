"""Author: Sagar Shelke
This is a client program which sends control packets emulation manager.
Here we are using google protocol buffers to serialize data since they are language neutral.

ctrl_buf.proto is protocol file with data structure we want to serialize.

To compile .proto file in linux
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/ctrl_buf.proto

e.g. consider you are in the same folder as that of .proto file
protoc -I=./ --python_out=./ ./ctrl_buf.proto
This gives ctrl_buf_pb2.py file in the same directory"""

import socket
import ctrl_buf_pb2


def send_pkt(cmd, non, ports, loc, seq, rloc):
    """This function creates socket and send a packet serialized using protocol buffer
    Arguments
    ---------
    cmd: string command
        currently one of "add_node","rm_node","status"
    non: number of nodes to add
    ports: a port list
    loc : location list
    seq : a boolean True or False
         if True, only one port is given and other are taken in sequence
    rloc: a boolean True or False
        if True, range of location is passed instead of passing individual x,y
    """

    host = "localhost"
    port_manager = 40001
    control = ctrl_buf_pb2.Control()    # create an object of compiled class
    control.cmd = cmd
    control.non = non
    control.ports.extend(ports)
    control.loc.extend(loc)
    control.seq = seq
    control.rloc = rloc

    data = control.SerializeToString()     # Serialized string

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port_manager))
    s.sendall(data)
    s.close()

if __name__ == "__main__":

    cmd_pass ="add_node"
    non_pass = 2
    ports_pass =[40005, 40006]
    loc_pass = [10, 10, 20, 30]
    seq_pass = False
    rloc_pass = False

    send_pkt(cmd_pass, non_pass, ports_pass, loc_pass, seq_pass, rloc_pass)

