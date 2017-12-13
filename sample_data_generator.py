"""Author: Sagar Shelke
This program is protobuf based data generator to check whether nodes accept packets in terms of protobuf or not.
"""
import socket
import data_buf_pb2

receiver_node_port = 40005
receiver_node_ip = "localhost"


def send_data(no_of_packets):
    """This function creates and sends packet over TCP.
    Arguments
    ---------
    no_of_packets: integer representing number of packets
    """
    generate = data_buf_pb2.Send()
    generate.nop = no_of_packets
    data = generate.SerializeToString()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket and send data
    s.connect((receiver_node_ip, receiver_node_port))
    s.sendall(data)
    s.close()


if __name__ == "__main__":
    send_data(3)
